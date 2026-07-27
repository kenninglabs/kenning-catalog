# Terraform

Infrastructure-as-code CLI, used to provision/deprovision cloud or local infra defined in `.tf` files.

- **Install docs:** https://developer.hashicorp.com/terraform/install
- **CLI reference:** https://developer.hashicorp.com/terraform/cli

Install prefers Homebrew (macOS and Linux) when it's present, falling back to the platform package manager otherwise -- see this catalog's `brew` tool.

## Verify

```bash
terraform version
```

## Common commands

```bash
terraform init       # download providers/modules, set up backend
terraform plan        # preview changes
terraform apply       # apply changes
terraform destroy     # tear down everything the state file tracks
```
