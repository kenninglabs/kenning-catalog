# Secrets Handling + PCI-DSS Dev Conventions

**Triggers:** about to commit/save anything that might contain a credential, key, or card data; writing a log/error message, ticket, or context doc from data that touches payments.

## Secrets

- **Never commit** API keys, tokens, passwords, private keys, `.env` files, service-account JSON, or connection strings with embedded credentials. `.gitignore` these by default: `.env`, `.env.*`, `*.pem`, `*.key`, `credentials.json`, `*_rsa`.
- **Reference by env var or secret manager, never hardcode.** In docs/examples use obviously-fake placeholders (`<TOKEN>`, `you@example.com`) — never a real-shaped key that could be mistaken for one.
- **Never print a secret's value** — not to logs, not to a chat response, not to a debug dump. Check presence only (`${VAR:+set}`), never the content.
- **Before a broad `git add`/`git add -A`, check what's actually staged.** A filename can look innocuous while its contents hold a token.

## If one leaks anyway

**Rotate it at the source immediately** — revoke and reissue. Assume it's compromised the moment it's pushed, even to a private repo. Rewriting git history (`filter-repo`/BFG) only stops *future* clones from getting it — it does not undo exposure to anyone who already pulled, forked, mirrored, or has it in CI logs/cached objects. Rotation is the fix; history-scrubbing is cleanup on top of that, never a substitute for it.

## PCI-DSS conventions (card data)

- **CVV/CVV2 is never stored, period** — not encrypted, not transiently, not in a log or debug dump, not even "just while investigating." This applies after authorization with no exception.
- **Never log or save a full PAN** (the card number) anywhere — app logs, error traces, tickets, context docs. If you must reference one while debugging, mask it first: first 6 + last 4 digits only (`453600XXXXXX0059`), matching PCI DSS's own display-masking rule. Save only the masked form, even in your own working notes.
- **Test/dev fixtures use published test PANs**, never real captured traffic: Visa `4111111111111111`, Mastercard `5555555555554444` — dummy numbers built for exactly this purpose.
- **Prefer tokenization.** If your payment processor offers a token in place of the PAN, use it — the real number then never touches your systems at all, which is the strongest scope reduction available.
- **Minimize the card-data environment.** Don't let a test/staging path casually carry real-looking card data through more systems than production actually needs to touch.
- **A real card number surfacing in a log/ticket/doc during debugging is an incident, not a formatting issue** — mask your own copy, and flag that the source (log storage, ticket system) needs its own retention/redaction review. Don't quietly fix your copy and call it handled.
