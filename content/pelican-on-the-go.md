Title: Pelican on the go
Date: 2015-04-15 21:08
Tags: python, pelican, meta

In this article, I describe my current set up for writing content for my pelican based sites on my phone.

<!-- PELICAN_END_SUMMARY -->

### Caveat lector

I use GitHub to deploy my pelican sites. For an overview of the set up, read the article [multi-player pelican]({filename}multi-player-pelican.md). While this article assumes a similar set up, it can be applied to just about any set up (with or without git). Just try to make sure you don't end up putting a *.git* directory on Dropbox. 

### Preamble

As I don't always want to grab my laptop to write new content, I'd like to be able to do so from my (android) phone and if it's not too much trouble, I'd like to be able to switch back and forth between my phone and my laptop.

### Editing markdown

First things first, let's find suitable a markdown editor for Android. There's a couple of them out there (Writeily, Jotter and Draft to name a few) but I decided to use [Draft](https://play.google.com/store/apps/details?id=com.mvilla.draft) because it can sync with Dropbox and I think it's generally the most competent markdown editor out there for Android.

This is not a requirement however. Any markdown, ReST or text editor that allows you to somehow sync the folder with a folder on your main PC will do. 

### Syncing with Dropbox

Now that that's settled, we'll have to find a way to keep everything in sync. I didn't want to keep the entire pelican projects in Dropbox. Also, git trees inside your Dropbox might or might not work but that doesn't seem like an elegant solution either way. So I investigated how to sync a folder outside the Dropbox directory with Dropbox. The answer was ridiculously simple, a symbolic link. If you create a symbolic link inside the Dropbox folder on your PC, the Dropbox client will follow that symlink and keep whatever folder it points at synchronised. So, start the terminal and create a symlink in the folder Draft created in your Dropbox account to the pelican *content* directory (my pelican install for blurringexistence.net resides in *~/Sites/blurringexistence.net*):

    ln -s ~/Sites/blurringexistence.net/content \
        ~/Dropbox/Draft/blurringexistence.net

Now, wait for Dropbox to finish synchronising the newly added content. 

### Editing content

Start Draft on your phone (or tablet) and initiate a sync with Dropbox. You should now see the content become available in Draft. I've enabled "Sync when app opens" and "Sync when a note is saved" in the settings of Draft to make sure both my phone and Dropbox are always kept up to date. Now, create or edit a file inside the content folder, save it, go back to your laptop and you can publish the article using your favorite git client.

### PS

In a next article, I will describe a way to extend the infrastructure we've created so far to be able to actually publish articles or pages from your phone without intervention from your laptop or PC.
