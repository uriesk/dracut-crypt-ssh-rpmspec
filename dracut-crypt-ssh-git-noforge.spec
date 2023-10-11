%define dracutlibdir %{_prefix}/lib/dracut
%global commit de3c2b9ffceae77f04b3aa2c05cf0f377f0c39a8

Name: dracut-crypt-ssh
Version: 1.0.8
Release: 2%{?dist}
Summary: A dracut module that adds ssh to the boot image (also known as earlyssh)
URL:     https://github.com/dracut-crypt-ssh/dracut-crypt-ssh
Source0: https://github.com/dracut-crypt-ssh/%{name}/archive/%{commit}.zip

%if 0%{?fedora} || 0%{?rhel}
Group: System Environment/Base
%endif
%if 0%{?suse_version}
Group: System/Base
%endif

License: GPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: dracut
BuildRequires: gcc
BuildRequires: libblkid-devel
Requires: dropbear
Requires: dracut
Requires: dracut-network
Requires: openssh


%description
Dracut initramfs module to start dropbear sshd on early boot to enter
encryption passphrase from across the internets or just connect and debug
whatever stuff there.

Idea is to use the thing on remote VDS servers, where full-disk encryption is
still desirable (if only to avoid data leaks when disks will be decomissioned
and sold by VDS vendor) but rather problematic due to lack of KVM or whatever
direct console access.

Authenticates users strictly by provided authorized_keys ("dropbear_acl"
option) file.

See dropbear(8) manpage for full list of supported restrictions there
(which are fairly similar to openssh).

Please read the README and configuration parameters in
/etc/dracut.conf.d/crypt-ssh.conf before use.


%prep
%autosetup -p1 -n %{name}-%{commit}


%build
%configure

make %{?_smp_mflags}


%install
%if 0%{?fedora} || 0%{?rhel}
rm -rf -- $RPM_BUILD_ROOT
%endif

make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf -- $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.md
%license COPYING COPYRIGHT
%config(noreplace) %{_sysconfdir}/dracut.conf.d/crypt-ssh.conf
%dir %{dracutlibdir}/modules.d/60crypt-ssh
%dir %{dracutlibdir}/modules.d/60crypt-ssh/helper
%{dracutlibdir}/modules.d/60crypt-ssh/module-setup.sh
%{dracutlibdir}/modules.d/60crypt-ssh/dropbear-start.sh
%{dracutlibdir}/modules.d/60crypt-ssh/dropbear-stop.sh
%{dracutlibdir}/modules.d/60crypt-ssh/50-udev-pty.rules
%{dracutlibdir}/modules.d/60crypt-ssh/helper/console_peek.sh
%{dracutlibdir}/modules.d/60crypt-ssh/helper/unlock
%{dracutlibdir}/modules.d/60crypt-ssh/helper/console_auth
%{dracutlibdir}/modules.d/60crypt-ssh/helper/unlock-reap-success.sh

%changelog
* Mon May 15 2023 uriesk <uriesk@posteo.de> - 1.0.7-3
- Build from commit f8127c

* Mon May 15 2023 uriesk <uriesk@posteo.de> - 1.0.7-2
- Build from git repo since we didn't get new Tags provided

* Thu Apr 26 2018 rbu <rbu@goodpoint.de> - 1.0.7-1
- Update to 1.0.7

* Thu Mar 08 2018 rbu <rbu@goodpoint.de> - 1.0.6-1
- Update to 1.0.6

* Thu Mar 08 2018 rbu <rbu@goodpoint.de> - 1.0.5-1
- Update to 1.0.5

* Thu Mar 08 2018 rbu <rbu@goodpoint.de> - 1.0.4-2
- Update to 1.0.4

* Sun Mar 06 2016 Robert Buchholz <rbu@fedoraproject.org> - 1.0.3-1
- Upgrade to 1.0.3

* Sat Feb 27 2016 Robert Buchholz <rbu@fedoraproject.org> - 1.0.2-7
- Rename project to crypt-ssh
- Clean up, use variables consistent with dracut spec
- Initial changelog entry, spec file based on Philippe Kueck and
  Michael Curtis, licensed under the "DO WHAT THE FUCK YOU WANT TO
  PUBLIC LICENSE"
