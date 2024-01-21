from terrabridge.gcp import SecretManagerSecret

sec = SecretManagerSecret("secret", state_file="terraform.tfstate")
print(sec.version().decode("utf-8"))
