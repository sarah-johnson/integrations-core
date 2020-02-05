# Configuration

-----

## GitHub

To avoid GitHub's public API rate limits, you need to set `github.user`/`github.token` in your config file or
use the `DD_GITHUB_USER`/`DD_GITHUB_TOKEN` environment variables.

Run `ddev config show` to see if your GitHub user and token is set.

If not:

1. Run `ddev config set github.user <YOUR_GITHUB_USERNAME>`
2. Create a [personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) with `public_repo` permissions
3. Run `ddev config set github.token` then paste the token
4. [Enable single sign-on](https://help.github.com/en/github/authenticating-to-github/authorizing-a-personal-access-token-for-use-with-saml-single-sign-on) for the token
