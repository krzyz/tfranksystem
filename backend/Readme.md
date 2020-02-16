# Setup
In the following, `$profile` is the name of AWS profile (for awscli) and `$stage` is the name of the stage to use. If using default profile, all $profile related attributes may be omitted.

To deploy backend, run:
```console
foo@bar:~$ sls deploy --stage $stage --aws-profile $profile
```

To create a first player, run the following ():
```console
foo@bar:~$ AWS_PROFILE=$profile STAGE=$stage python -m tools.create_player
```