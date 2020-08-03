<p align="center">
  <img src="images/HDRUK_LOVE_OPEN_SOURCE.png">
</p>

# HDR UK Open Source Projects (4)

### GATEWAY-MVP (4)
1. [Gateway-Frontend](https://github.com/HDRUK/Gateway-Frontend)
2. [Gateway-Auth-Server](https://github.com/HDRUK/Gateway-Auth-Server)
3. [Gateway-Middleware](https://github.com/HDRUK/Gateway-Middleware)
4. [Gateway-DB](https://github.com/HDRUK/Gateway-DB)

---
### How to add projects

1. Create a [Github.com account](https://github.com/join) if you do not have one already
2. Create a [fork of this project](https://github.com/HDRUK/oss).
3. Edit the [oss_projects.yml](data/oss_projects.yml) file and add an entry for your project using this template:
   ```yaml
   - name: 'Project Awesome'
     description: 'Describe what your project is about'
     url: 'https://github.com/YOUREPO (Provide your Github Repo URL)'
     keywords: [ 'example', 'keyword' ]
     categories: ['HDR UK', 'themes' ]
   ```
4. Commit the changes to your fork and submit a Pull request against this project.

We'll review all requests and accept them according to HDR UK's policies. If accepted, your project will be listed below