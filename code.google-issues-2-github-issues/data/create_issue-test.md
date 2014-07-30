
#### mapping the code.google.com issue into github issue

```BASH
curl	-s
	--user "mbohun"
	--request POST
	--data '{
			"title": "only a test issue, created using github api v3 from BASH and curl",
			"body": "This is the issues body, description, very deep in all important details.",
			"assignee": "nickdos",
			"labels": [
					"Label1",
					"Label2"
				]
		}'

	https://api.github.com/repos/atlasoflivingaustralia/biocache-hubs/issues
```
