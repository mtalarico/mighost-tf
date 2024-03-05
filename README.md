# mighost-tf
An example terraform module that automatically provision one or more migration hosts w/ Mongosync. The current setup sets up a Private Endpoint and either one or N migration hosts depending on if you provide the "source_shard_map" array variable.

<hr>

**⚠️ This is an example terraform script, it is a WIP and has not been fully tested or vetted. It is not an official MongoDB product. As with all software, use with discretion and test thoroughly.**

<hr>

# TODO:
- [ ] improve UX (right now this module provisions a Private Endpoint that is required to get the PE string of the cluster on the source/dest... chicken and egg situation)
- [ ] expand this documentation
- [ ] make the os_id an enum




