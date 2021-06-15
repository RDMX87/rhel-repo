#!/bin/bash

cat pkgs.txt | while read pkg; do
  if [[ ! -z $pkg ]]; then
    check_update_str=$(yum check-update $pkg | grep $pkg)
    if [[ ! -z $check_update_str ]]; then
      pkg_file=$(echo $check_update_str | awk '{ print $1 }' | cut -d. -f1)
      pkg_arch=$(echo $check_update_str | awk '{ print $1 }' | cut -d. -f2)
      pkg_version=$(echo $check_update_str | awk '{ print $2 }')
      pkg_file_name_version=$(echo $pkg_version | cut -d: -f2)
      if [[ ! -e "7/os/x86_64/Packages/$pkg_file-$pkg_file_name_version.$pkg_arch.rpm" ]]; then
        yum update --downloadonly --downloaddir=7/os/x86_64/Packages $pkg_file-$pkg_version.$pkg_arch
      fi
    fi
  fi
done

createrepo --update 7/os/x86_64

chown -R user:user 7/os/x86_64
