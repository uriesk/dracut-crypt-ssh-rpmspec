%define dracutlibdir %{_prefix}/lib/dracut

Name: dracut-earlyssh
Version: 1.0.2
Release: 7%{?dist}

Summary: A dracut module that adds ssh to the boot image (also known as earlyssh)
%if 0%{?fedora} || 0%{?rhel}
Group: System Environment/Base
%endif
%if 0%{?suse_version}
Group: System/Base
%endif

# FIXME: "DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE"
License: GPLv2+
# FIXME: project page
URL: https://github.com/philfry/%{name}
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: dracut libblkid-devel gcc
Requires: dropbear dracut dracut-network openssh


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
/etc/dracut.conf.d/earlyssh.conf before use.


%prep
%setup -q -n %{name}-%{version}


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
%doc README.md COPYING
%config(noreplace) %{_sysconfdir}/dracut.conf.d/earlyssh.conf
%dir %{_libexecdir}/dracut-earlyssh
%{_libexecdir}/dracut-earlyssh/unlock
%{_libexecdir}/dracut-earlyssh/console_auth
%dir %{dracutlibdir}/modules.d/60earlyssh
%{dracutlibdir}/modules.d/60earlyssh/module-setup.sh
%{dracutlibdir}/modules.d/60earlyssh/console_peek.sh
%{dracutlibdir}/modules.d/60earlyssh/unlock-reap-success.sh
%{dracutlibdir}/modules.d/60earlyssh/50-udev-pty.rules
%if 0%{?el6}
# %{dracutlibdir}/modules.d/60earlyssh/dummyroot
# %{dracutlibdir}/modules.d/60earlyssh/check
# %{dracutlibdir}/modules.d/60earlyssh/install
# %dir %{dracutlibdir}/modules.d/91cryptsettle-patch
# %{dracutlibdir}/modules.d/91cryptsettle-patch/check
# %{dracutlibdir}/modules.d/91cryptsettle-patch/install
# %{dracutlibdir}/modules.d/91cryptsettle-patch/module-setup.sh
%endif

%changelog
* Sat Feb 27 2016 Robert Buchholz <rbu@fedoraproject.org> - 1.0.2-7
- Clean up, use variables consistent with dracut spec
- Initial changelog entry, spec file based on Philippe Kueck and
  Michael Curtis, licensed under the "DO WHAT THE FUCK YOU WANT TO
  PUBLIC LICENSE"
