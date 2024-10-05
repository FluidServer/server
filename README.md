<p align="center">

<h1 align="center"><img src="data/favicon.png" width="30px" alt="Icon" title="Icon">FluidServer</h1>

<p align="center">
<img src="https://img.shields.io/github/license/FluidServer/server" alt="License" title="License" >
</p>

</p>

> Open source scalable POS-system server

Is it just me or are most commercial POS-systems garbage? Want something better in life? Something made to be good? Try FluidServer!

FluidServer is a scalable POS-system for - well - people who don't hate themselves. It makes it easier for system administrators and developer to use and implement - it's also more scalable than most POS-systems.

<!--
# Installation
## Windows

Go to `fs.biitle.nl` and click on <button style="background-color: #19b4fe; border: 0px solid black; border-radius: 3px; padding: 3px 6px; color: white;">Download FluidServer</button>.

Open the installer and follow the steps, after that, you can run FluidServer.

## Linux (and Mac)
Run `curl fs.biitle.nl/install.sh | bash` to install FluidServer, follow the steps and run FluidServer from where you installed it to.

## Installerless
Clone the git repo by typing `git clone https://github.com/fgclue/fluidserver` and run the `make install`. Run `python api.py` to run FluidServer.
-->

# Usage Example

Sending a request to `/api/product/1` will return the product data in this format:
`Name|Price|Type (UN/KG)|Controlled (for pharmacies)`.

If you want to host in a port different than the default `1618`, just run fluid server with the argument `--port` or `-p` and your port. However, using ports below 1024 are not recommended as those ports are considered "privileged ports" and require root to use.

# Integration
If you are a developer of a POS-system then you can easily integrate FluidServer by reading the [documentation](/docslinkhere).

Also, you can use Swagger UI to test the APIs from your browser (while running FluidServer of course.)

# Meta
Built by clue <<lost@biitle.nl>>.

Distributed under the MIT license.

# Contributing
1. Fork the repo (https://github.com/FluidServer/server)
2. Create your feature branch (`git checkout -b feature/yournewfeature`)
3. Commit your changes (`git commit -am 'Add some change'`)
4. Push to the branch (`git push origin feature/yournewfeature`)
5. Create a new pull request