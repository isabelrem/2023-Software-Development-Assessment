# What I did with my extension
* modified setup.sh so that the sql database was correctly setup with a longtext field.
* Removed Cloud SQL setup as an option as not routinely working - user will now need to be able to run docker containers with sudo permissions
* reset.sh now removes specifically the docker containers / volumes / images / networks associated to PanelSearch, instead of every docker item the computer has. 
* simplified setup.sh to proceed straight to docker setup rather than querying the user which SQL db they want to use
* modified gitignore so only contents of panelsearch_downloads folder is ignored by git, not the folder itself. Modified setup.sh so that the contents of docker panelsearch_downloads is copied into the local panelsearch_downloads, rather than the local panelsearch_downloads directory being overwritten entirely.
* as above but with the bed_files directory.
* created panelsearch.sh file - combined setup.sh and rerun.sh, hopefully making an easier user experience bc their input for running for the first time or rerunning the app will be no different.
* app now runs on a loop so users wanting to make multiple searches at one time only have to run the panelsearch.sh or reset.sh file once.
* removed all mention of 'cloud' from the code, since no cloud db is used anymore.
* got the app to ask for the genome build before the test code / test name
* cleaned up print and errant comments.
* have added transcript field which contains actual transcript info - but already present in more readable form in BED file I've noticed - more sense to remove transcript field?