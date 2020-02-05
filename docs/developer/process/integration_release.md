# Integration release

-----

Each Agent integration has its own release cycle. Many integrations are actively developed and released often while
some are rarely touched (usually indicating feature-completeness).

## Versioning

All releases adhere to [Semantic Versioning](https://semver.org).

Tags in the form `<INTEGRATION_NAME>-<VERSION>` [are added](../meta/cd.md) to the Git repository. Therefore, it's
possible to checkout and build the code for a certain version of a specific check.

## Setup

[Configure](../ddev/configuration.md#github) your GitHub auth.

## Identify changes

!!! note
    If you already know which integration you'd like to release, skip this section.

To see all checks that need to be released, run `ddev release show ready`.

## Steps

1. Checkout and pull the most recent version of the `master` branch.

    ```
    git checkout master
    git pull
    ```

    !!! danger "Important"
        Not using the latest version of `master` may cause errors in the [build pipeline](../meta/cd.md).

1. Review which PRs were merged in between the latest release and the `master` branch.

    ```
    ddev release show changes <INTEGRATION>
    ```

    You should ensure that PR titles and changelog labels are correct.

1. Create a release branch from master (suggested naming format is `<USERNAME>/release-<INTEGRATION_NAME>`).
   This has the purpose of opening a PR so others can review the changelog.

    !!! danger "Important"
        It is critical the branch name is not in the form `<USERNAME>/<INTEGRATION_NAME>-<NEW_VERSION>` because one of
        our Gitlab jobs is triggered whenever a Git reference matches that pattern, see !3843 & !3980.

1. Make the release.

    ```
    ddev release make <INTEGRATION>
    ```

    You may need to touch your Yubikey multiple times.

    This will automatically:

    - update the version in `<INTEGRATION>/datadog_checks/<INTEGRATION>/__about__.py`
    - update the changelog
    - update the `requirements-agent-release.txt` file
    - update [in-toto metadata](../meta/cd.md)
    - commit the above changes

1. Push your branch to GitHub and create a pull request.

    1. Update the title of the PR to something like `[Release] Bumped <INTEGRATION> version to <VERSION>`.
    1. Ask for a review in Slack.

1. Merge the pull request after approval.

### PyPI

If you released `datadog_checks_base` or `datadog_checks_dev` then you will need to upload to [PyPI](https://pypi.org)
for use by [integrations-extras](https://github.com/DataDog/integrations-extras).

```
ddev release upload datadog_checks_[base|dev]
```

### Metadata

You need to run certain jobs if any changes modified integration metadata. See the
[Declarative Integration Pipeline](https://github.com/DataDog/devops/wiki/Declarative-Integration-Pipeline) wiki.

## Bulk releases

To create a release for every integration that has changed, use `all` as the integration name in the `ddev release make`
step above.

```
ddev release make all
```

You may also pass a comma-separated list of checks to skip using the `--exclude` option, e.g.:

```
ddev release make all --exclude datadog_checks_dev
```

## Betas

Creating pre-releases is the same workflow except you do not open a pull request but rather release directly from a branch.

In the `ddev release make` step set `--version` to `[major|minor|patch],[rc|alpha|beta]`.

For example, if the current version of an integration is `1.1.3`, the following command will bump it to `1.2.0-rc.1`:

```
ddev release make <INTEGRATION> --version minor,rc
```

After pushing the release commits to GitHub, run:

```
ddev release tag <INTEGRATION>
```

This manually triggers the [build pipeline](../meta/cd.md).

To increment the version, omit the first part, e.g.:

```
ddev release make <INTEGRATION> --version rc
```

## New integrations

To bump a new integration to `1.0.0` if it is not already there, run:

```
ddev release make <INTEGRATION> --new
```

To ensure this for all integrations, run:

```
ddev release make all --new
```

If a release was created, run:

```
ddev agent requirements
```

## Troubleshooting

- If you encounter errors when signing with your Yubikey, ensure you ran `gpg --import <YOUR_KEY_ID>.gpg.pub`.
