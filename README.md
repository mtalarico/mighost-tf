# mighost-tf
An example terraform module that automatically provision one or more migration hosts w/ Mongosync. The current setup sets up either one or N migration hosts depending on if you provide the "source_shard_map" array variable. A small python-based wrapper for controlling all N mongosync api's is provided as well.

<hr>

**⚠️ These are example terraform/python script. They are a WIP and has not been fully tested or vetted. This repository and its contents are not official MongoDB products. As with all software, use with discretion and test thoroughly.**

<hr>

# TODO:
- [x] improve UX (right now this module provisions a Private Endpoint that is required to get the PE string of the cluster on the source/dest... chicken and egg situation)
     - split the infrastructure and migration host into separate terraform scripts with different lifetimes
- [ ] expand this documentation
- [ ] make the os_id an enum




