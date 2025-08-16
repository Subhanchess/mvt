# MVT iOS Quickstart

This quickstart shows how to use [Mobile Verification Toolkit (MVT)](https://github.com/mvt-project/mvt) to scan an iOS device on macOS.

## Install on macOS

```sh
# with Homebrew
brew install mvt

# or using pipx
brew install pipx  # if pipx is not installed
pipx install mvt
```

## Create an encrypted backup

1. Connect the iOS device to the Mac.
2. Create an **encrypted** backup using Finder or the command below:

```sh
idevicebackup2 backup --full --encrypt --password "$BACKUP_PASS" backup/
```

## Decrypt the backup

```sh
mvt-ios decrypt-backup -p "$BACKUP_PASS" -d decrypted/ backup/
```

## Fetch indicators and scan

```sh
mvt-ios download-iocs
mvt-ios check-backup --output mvt_out decrypted/
```

## Security notes

- Only analyze devices with the owner's explicit consent.
- A match with an indicator does **not** confirm an infection.
- Do not commit generated backups or scan results to any repository.

All commands above are ready to copy and run. Adjust paths and passwords as needed.
