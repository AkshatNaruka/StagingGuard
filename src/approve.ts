import { ApprovalStore } from './runtime.js';

const requestId = process.argv[2];
if (!requestId) { console.error('Usage: npm run approve -- <approvalRequestId> [--yes]'); process.exitCode = 1; }
else {
  try {
    const store = new ApprovalStore('.local/approvals');
    const request = await store.review(requestId);
    console.log(JSON.stringify(request, null, 2));
    if (process.argv.includes('--yes')) { await store.approve(requestId); console.log('Approved this exact synthetic reply once. Retry it before the task expires.'); }
    else console.log('Review the text above, then add --yes to approve. This command belongs to the human reviewer.');
  } catch { console.error('Request missing, invalid, or expired. Start a new request and review its current ID.'); process.exitCode = 1; }
}
