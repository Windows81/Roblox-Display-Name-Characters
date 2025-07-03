What characters can you use in a Rōblox display name? Check the [`./csv`](./csv) files to see for yourself.

**You need to have `ROBLOSECURITY` set as an environment variable.**

All web requests come from California, USA on an _account location_ from North Korea.

**According to the schema, any values where `code` is either -1 or 4 means that the character can be used _at all_ in a username.**

Any values where `code` equals -1 means that a display name with three times the character can be used.

For example: I can pick the display name `CCC` because:

| iden | char | code |
| ---- | ---- | ---- |
| 67   | C    | -1   |

Other relevant `code` values include:

- `3`: `Display name contains invalid characters`
- `4`: `Display name has been moderated`
