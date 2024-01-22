# terrabridge

![CI](https://github.com/launchflow/terrabridge/actions/workflows/python_ci.yaml/badge.svg)
[![Python version](https://badge.fury.io/py/terrabridge.svg)](https://pypi.org/project/terrabridge)
[![codecov](https://codecov.io/gh/launchflow/terrabridge/graph/badge.svg?token=slFk4lUP2h)](https://codecov.io/gh/launchflow/terrabridge)

Terrabridge bridges the gap between Terraform and applicatoin code. With Terrabridge you simply provide your terraform state file to the library and all information will be loaded allowing you to easily access your resources. This allows you to truly keep your infrastructure configuration in one place. 

TODO: add link to docs

```python
from terrabridge.gcp import SecretManagerSecret

sec = SecretManagerSecret("secret", state_file="terraform.tfstate")
print(sec.version().decode("utf-8"))

```

## Installation

```bash
pip install terrabridge
```

## Supported Providers and Languages

Python in the first language we support however we plan to support more languages in the future. We are always happy to accept contributions for new languages and providers.

|           | **python** | **golang** | **java** | **typescript** |
|-----------|------------|------------|----------|----------------|
| **gcp**   | ✅          | ❌          | ❌        | ❌              |
| **aws**   | 🚧          | ❌          | ❌        | ❌              |
| **azure** | ❌          | ❌          | ❌        | ❌              |