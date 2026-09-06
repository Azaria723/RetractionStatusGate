import { createClient } from "../../OpenSourceMicroBounty/frontend/node_modules/genlayer-js/dist/index.js";
import { studionet } from "../../OpenSourceMicroBounty/frontend/node_modules/genlayer-js/dist/chains/index.js";
import { createHash } from "node:crypto";

const contract = process.env.CONTRACT_ADDRESS;
const expectedHash = "3e143546d6c66ae6102aa2e47f1e7e24a0dc2dfeb6f674f1666a4a84a51c0bc0";
if (!/^0x[0-9a-fA-F]{40}$/.test(contract || "")) throw new Error("Set CONTRACT_ADDRESS");

const client = createClient({ chain: studionet });
const schema = await client.getContractSchema(contract);
const code = await client.getContractCode(contract);
const sourceHash = createHash("sha256").update(code, "utf8").digest("hex");

console.log(`contract=${contract}`);
console.log(`chain_id=${studionet.id}`);
console.log(`schema_methods=${JSON.stringify(Object.keys(schema || {}).sort())}`);
console.log(`deployed_source_sha256=${sourceHash}`);
console.log(`expected_source_sha256=${expectedHash}`);
console.log(`source_parity=${sourceHash === expectedHash}`);
console.log(`counts=${await client.readContract({ address: contract, functionName: "get_counts", args: [] })}`);
