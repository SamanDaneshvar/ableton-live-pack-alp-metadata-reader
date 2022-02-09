# Ableton Live Pack (ALP) Metadata Reader
This Python script reads your ALP files and generates a spreadsheet report of the important metadata inside those files (i.e., pack name, vendor name, version).

## What are Ableton Live Packs (ALP files)?
Ableton Live is a very popular and powerful Digital Audio Workstation (DAW). It has hundreds of instruments, sounds, and effects (called *packs*) available for purchase and download. Each Ableton Live Pack comes in the form of a *.ALP* file.

## What is this script useful for?
If you have a .ALP file on your computer and are not sure which pack it belongs to or who is its creator, or what is the distribution version of it, you are pretty much out of luck! Because your operating system won't show that information in the metadata of the file (under Properties, for instance) and Ableton itself does not have the option to show you that information. The only thing that Ableton does is to install the pack. So, if you open the .ALP file, Ableton Live will begin to install that pack, without even showing you the name and version of the pack.

If you don't need to know the name of your pack, its vendor, and its distribution version, then this script is not for you!

## But, there has to be a way to find that information. Right?
Yes. The only thing you can do (other than using this tool) is to open your .ALP file in a text editor. There, you will be able to see a block of text like below:

```
FolderConfigData
{
  String PackUniqueID = "www.ableton.com/00";
  String PackDisplayName = "Name of The Pack";
  String PackVendor = "Name of The Vendor";
  Int PackMinorVersion = 21;
  Int PackMajorVersion = 8;
  Int PackRevision = 38398;
  Int ProductId = 000;
  Int MinSoftwareProductId = 0;
}
```

or:

```
"patcher" : 	{
    "fileversion" : 1,
    "appversion" : 		{
        "major" : 8,
        "minor" : 21,
        "revision" : 38398,
        "architecture" : "x64"
    }
```

As you can see, the metadata is written inside the file. This blob of text is often at the very beginning of the file, but that's not always the case.

## Then, how does this Python script help?
Well, it makes things much easier and faster.
- This script takes a directory address from you, and processes any .ALP file that exists directly under that directory.
- For every file, it finds the above-mentioned blob of text, and extracts the information that matters to us.
- In the end, it generates a report.csv file, which you can open in Microsoft Excel, Google Sheets, or your favorite text/spreadsheet editor.
- In the report file, you will see four columns: 
  - Filename
  - Name: Name of the pack
  - Vendor: Name of the vendor of the pack
  - Version: In the form of v[major].[minor] r[Revision]. In the example above: v8.21 r38398
 - Note that this script does not read the whole file——just a few lines until it reaches the metadata blob, as described above.

## Final thoughts
This is quite an uncommon task, so I don't expect many people to need this script. Nonetheless, I needed it so I wrote it, and now I'm putting it out there so that if someone was looking, they too can make use of it.

If you needed more help using the script or modifying my code, feel free to reach out to me. Enjoy making music!
