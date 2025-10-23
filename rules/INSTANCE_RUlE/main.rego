package rules.INSTANCE_RUlE

input_type := "tf"

resource_type := "aws_instance"

metadata := {
	"id": "INSTANCE_RUlE",
	"severity": "critical",
	"title": "No public ec2 instances",
	"description": "We are not allowing public ips to be associated with our instances",
	"product": ["iac"],
}

deny[info] {
	# TODO: add conditions so that this rule only returns when input is invalid. For example:
	# input.some_property == "bad value"
	info := {"resource": input}
}
