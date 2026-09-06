import { createClient } from "../../OpenSourceMicroBounty/frontend/node_modules/genlayer-js/dist/index.js";
import { studionet } from "../../OpenSourceMicroBounty/frontend/node_modules/genlayer-js/dist/chains/index.js";
import { TransactionStatus } from "../../OpenSourceMicroBounty/frontend/node_modules/genlayer-js/dist/types/index.js";
import { privateKeyToAccount } from "../../OpenSourceMicroBounty/frontend/node_modules/viem/_esm/accounts/index.js";

const contract = process.env.CONTRACT_ADDRESS;
const requesterKey = process.env.REQUESTER_PRIVATE_KEY;
if (!/^0x[0-9a-fA-F]{40}$/.test(contract || "")) throw new Error("Set CONTRACT_ADDRESS");
if (!requesterKey) throw new Error("Set REQUESTER_PRIVATE_KEY");

const requester = privateKeyToAccount(requesterKey.startsWith("0x") ? requesterKey : `0x${requesterKey}`);
const reader = createClient({ chain: studionet });
const writer = createClient({ chain: studionet, account: requester });
const transactions = [];
const read = async (functionName, args = []) => reader.readContract({ address: contract, functionName, args });
const parse = async (functionName, args = []) => JSON.parse(await read(functionName, args));

const write = async (functionName, args = []) => {
  const hash = await writer.writeContract({ address: contract, functionName, args });
  console.log(`${functionName}_tx=${hash}`);
  let receipt;
  for (let attempt = 1; attempt <= 18; attempt++) {
    try {
      receipt = await reader.waitForTransactionReceipt({ hash, status: TransactionStatus.FINALIZED });
      break;
    } catch (error) {
      if (attempt === 18) throw error;
      await new Promise((resolve) => setTimeout(resolve, 5000));
    }
  }
  console.log(`${functionName}_status=${receipt.status_name || receipt.status}`);
  transactions.push({ functionName, hash });
};

const cases = [
  { doi: "10.5555/active-001", verdict: "ACTIVE", digest: "71ac69e7891c53195d0740aeade7cc086a499566b1f225343c631c8701737050" },
  { doi: "10.5555/retracted-002", verdict: "RETRACTED", digest: "42361f9b501742d1a360bfac540915c4c3eebcfc9c3d92bcf50bca9e8b30677f" },
  { doi: "10.5555/concern-003", verdict: "EXPRESSION_OF_CONCERN", digest: "6aff3b789e7d9573529b8b2559b7f730063d573779b4832ee5aa9bebe65a49be" },
  { doi: "10.5555/missing-004", verdict: "UNAVAILABLE", digest: "", identity: "NOT_CHECKED" },
];

console.log(`contract=${contract}`);
console.log(`requester=${requester.address}`);
let counts = await parse("get_counts");
console.log(`counts_before=${JSON.stringify(counts)}`);
if (counts.publisher_count !== 1) throw new Error(`Publisher is not registered: ${JSON.stringify(counts)}`);
const publisher = await parse("get_publisher", [0n]);
console.log(`publisher=${JSON.stringify(publisher)}`);
if (publisher.publisher_key !== "DEMO-PUBLISHER" || publisher.doi_prefix !== "10.5555" || publisher.active !== 1) {
  throw new Error(`Unexpected publisher: ${JSON.stringify(publisher)}`);
}

for (let index = 0; index < cases.length; index++) {
  const item = cases[index];
  counts = await parse("get_counts");
  if (counts.check_count <= index) await write("request_status_check", [item.doi]);
  let check = await parse("get_check", [BigInt(index)]);
  if (check.doi !== item.doi) throw new Error(`Unexpected DOI at ${index}: ${JSON.stringify(check)}`);
  if (check.status === 0) await write("assess_status", [BigInt(index)]);
  check = await parse("get_check", [BigInt(index)]);
  console.log(`check_${index}=${JSON.stringify(check)}`);
  const diagnostics = JSON.parse(check.diagnostics);
  if (check.status !== 1 || check.verdict !== item.verdict || check.record_sha256 !== item.digest || diagnostics.identity !== (item.identity || "MATCH")) {
    throw new Error(`Case ${index} failed: ${JSON.stringify(check)}`);
  }
}

// Direct contract regression tests: finalized failure returns must not mutate counters.
const beforeFailures = await parse("get_counts");
await write("request_status_check", ["10.9999/unknown"]);
const afterUnknownPrefix = await parse("get_counts");
if (JSON.stringify(afterUnknownPrefix) !== JSON.stringify(beforeFailures)) throw new Error("Unknown-prefix failure mutated state");
console.log(`unknown_prefix_no_mutation=${JSON.stringify(afterUnknownPrefix)}`);

await write("request_status_check", ["10.5555/../../secret"]);
const afterInjection = await parse("get_counts");
if (JSON.stringify(afterInjection) !== JSON.stringify(beforeFailures)) throw new Error("Injection failure mutated state");
console.log(`path_injection_no_mutation=${JSON.stringify(afterInjection)}`);

console.log(`counts_after=${await read("get_counts")}`);
console.log(`transactions=${JSON.stringify(transactions)}`);
