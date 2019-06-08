# GSoC 19 POW BitTorrent Client (1):

A BitTorrent Client to create, seed and download from .torrent files. Coupled with Data Integrity and Authenticity checks!

## Getting Started

This will guide you through setting up this BitTorrent client, this repository is split into 2 parts:

#### 1) Uploading:
This involves generating the Message Digest for Data integrity, creating .torrents and seeding the contents to other BitTorrent peers.

#### 2) Downloading:
This involves selecting .torrent files, downloading the contents from peers into local machine and running Data Integrity checks.  


## Set it up!

### For Uploading:

- python libtorrent used here.

[python-libtorrent requires python2 and has package manager support for only Debian.]
```
sudo apt install python-libtorrent
```
- To create the Message Digest of the contents, create a .torrent file of those contents and then start seeding them.
```
python2 Uploading/seed_final.py
```
( Specify the file/folder withing the Uploading directory as shown here & then let it seed indefinitely. A .torrent file will be created within the Uploading Directory)  

![](images/seeding.png)


### For Downloading:
- Install modules within requirements.txt
```
pip3 install -r requirements.txt 

```
- Start the BitTorrent Download daemon:

```
python3 Downloading/torrent_cli.py start &
```

- Add the torrent file and the directory to download contents into:

```
python3 Downloading/torrent_cli.py add '.torrent file' -d 'Download directory'
```
- To watch the download progress use: (ctrl + c to exit view):
```
watch python3 torrent_cli.py status
```

![](images/downloading.png)

- After waiting for 100% download completion, check for data integrity:
```
python2 integrity.py 'path of .torrent file' 'Path of downloaded contents'
```
(Data integrity check shown below!)

![](images/done.png)



## Acknowledgments

* [Borzunov](https://github.com/borzunov/bit-torrent) - The Downloading portion of client! 

## Other


* [Torrents](https://eztv.io/) - Webpage to access larger, better seeded content.

