%if %{?WITH_SELINUX:0}%{!?WITH_SELINUX:1}
%define WITH_SELINUX 1
%endif

Summary: Displays the users logged into machines on the local network
Name: rusers
Version: 0.17
Release: 59%{?dist}
License: BSD
Group: System Environment/Daemons
Source: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-rusers-%{version}.tar.gz
Source1: rusersd.init
Source2: rstatd.tar.gz
Source3: rstatd.init
Patch0: rstatd-jbj.patch
Patch1: netkit-rusers-0.15-numusers.patch
Patch2: netkit-rusers-0.17-2.4.patch
Patch3: netkit-rusers-0.17-includes.patch
Patch4: netkit-rusers-0.17-truncate.patch
Patch5: netkit-rusers-0.17-stats.patch
Patch6: netkit-rusers-0.17-rstatd-no-static-buffer.patch
Patch7: netkit-rusers-0.17-strip.patch
Patch8: netkit-rusers-0.17-rup.patch
Patch9: netkit-rusers-0.17-rup-timeout.patch
Patch10: netkit-rusers-0.17-procps.patch
Patch11: netkit-rusers-0.17-rup-stack.patch
Patch12: netkit-rusers-0.17-bigendian.patch
Patch13: netkit-rusers-0.17-return.patch
Patch14: netkit-rusers-0.17-procdiskstats.patch
Patch15: netkit-rusers-0.17-rusersd-droppriv.patch
Buildroot: %{_tmppath}/%{name}-root
BuildRequires: procps libselinux-devel

%description
The rusers program allows users to find out who is logged into various
machines on the local network.  The rusers command produces output
similar to who, but for the specified list of hosts or for all
machines on the local network.

Install rusers if you need to keep track of who is logged into your
local network.

%package server
Summary: Server for the rusers protocol.
Group: System Environment/Daemons
Requires(pre): /sbin/chkconfig
Requires: portmap

%description server
The rusers program allows users to find out who is logged into various
machines on the local network.  The rusers command produces output
similar to who, but for the specified list of hosts or for all
machines on the local network. The rusers-server package contains the
server for responding to rusers requests.

Install rusers-server if you want remote users to be able to see
who is logged into your machine.

%prep
%setup -q -n netkit-rusers-%{version} -a 2
%patch0 -p1 -b .jbj
%patch1 -p1 -b .numusers
%patch2 -p1 -b .2.4
%patch3 -p1 -b .includes
%patch4 -p1 -b .truncate
%patch5 -p1 -b .stats
%patch6 -p1 -b .rstatd-no-static-buffer
%patch7 -p1 -b .strip
%patch8 -p1 -b .rup
%patch9 -p1 -b .rup-timeout
%patch10 -p1 -b .procps
%patch11 -p1 -b .rup-stack
%patch12 -p1 -b .bigendian
%patch13 -p1 -b .return
%patch14 -p1 -b .procdiskstats
%patch15 -p1 -b .dropprivs

%build
cat > MCONFIG <<EOF
# Generated by configure (confgen version 2) on Wed Jul 17 09:33:22 EDT 2002
#

BINDIR=%{_bindir}
SBINDIR=%{_sbindir}
MANDIR=%{_mandir}
BINMODE=755
DAEMONMODE=755
MANMODE=644
PREFIX=/usr
EXECPREFIX=/usr
INSTALLROOT=
CC=cc
CFLAGS=${RPM_OPT_FLAGS} -fPIC -Wall -W -Wpointer-arith -Wbad-function-cast -Wcast-qual -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations -Wnested-externs -Winline 
LDFLAGS=-pie
LIBS=
USE_GLIBC=1

EOF

make
%if %{WITH_SELINUX}
make LIBS="-lselinux" -C rpc.rstatd
%else
make -C rpc.rstatd
%endif


%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,8}
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d

make INSTALLROOT=${RPM_BUILD_ROOT} install
make INSTALLROOT=${RPM_BUILD_ROOT} install -C rpc.rstatd

install -m 755 %SOURCE1 ${RPM_BUILD_ROOT}/etc/rc.d/init.d/rusersd
install -m 755 %SOURCE3 ${RPM_BUILD_ROOT}/etc/rc.d/init.d/rstatd

%clean
rm -rf ${RPM_BUILD_ROOT}

%post server
/sbin/chkconfig --add rusersd
/sbin/chkconfig --add rstatd

%preun server
if [ $1 = 0 ]; then
    /sbin/chkconfig --del rusersd
    /sbin/chkconfig --del rstatd
fi

%files
%defattr(-,root,root)
%doc README
%{_bindir}/rup
%{_bindir}/rusers
%{_mandir}/man1/*

%files server
%defattr(-,root,root)
%{_mandir}/man8/*
%{_sbindir}/rpc.rstatd
%{_sbindir}/rpc.rusersd
%config /etc/rc.d/init.d/rusersd
%config /etc/rc.d/init.d/rstatd

%changelog
* Fri Feb 26 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 0.17-59
- added README
- Related: #543948

* Wed Feb 24 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 0.17-58
- fixed rusersd initscript
- fixed rstatd initscript
- Resolves: #567957, #567958

* Fri Jan  8 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 0.17-57
- fixed rpmlint warnings
- Resolves: #543948

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.17-56.1
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep  4 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 0.17-54
- modified truncate patch to work with fuzz=0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.17-53
- Autorebuild for GCC 4.3

* Tue Sep 18 2007 Jiri Moskovcak <jmoskovc@redhat.com> 0.17-52
- Fixed init script to work properly with rpcbind

* Sat Sep 15 2007 Steve Dickson <steved@redaht.com> 0.17-51
- Removed portmap dependency and re-worked when the user
  privilege are drop; allowing port registration with
  rpcbind. (#247985)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.17-50
- Rebuild for selinux ppc32 issue.

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 0.17-49
- rebuild for toolchain bug

* Mon Jul 23 2007 Jiri Moskovcak <jmoskovc@redhat.com> 0.17-48
- Fixed init scripts to comply with LSB standard
- Resolves: #247047

* Wed Aug 09 2006 Phil Knirsch <pknirsch@redhat.com> 0.17-47
- Modified the RHEL3 procpartitions patch to work on recent 2.6 kernels (#201839)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.17-46.1
- rebuild

* Tue Mar 21 2006 Phil Knirsch <pknirsch@redhat.com> - 0.17-46
- Included fix for correct return values for rup (#177419)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.17-45.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.17-45.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep 07 2005 Phil Knirsch <pknirsch@redhat.com> 0.17-45
- Fixed 64bit bigendian problem in rpc.rstatd (#130286)

* Wed May 04 2005 Phil Knirsch <pknirsch@redhat.com> 0.17-44
- Fixed rup stack problem (#154396)

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 0.17-43
- bump release and rebuild with gcc 4

* Fri Feb 18 2005 Phil Knirsch <pknirsch@redhat.com> 0.17-42
- rebuilt

* Mon Jul 12 2004 Phil Knirsch <pknirsch@redhat.com> 0.17-41
- Bump release.

* Mon Jul 12 2004 Phil Knirsch <pknirsch@redhat.com> 0.17-40
- Made patch to make rpc.rstatd independant of procps (#127512)

* Tue Jun 29 2004 Phil Knirsch <pknirsch@redhat.com> 0.17-39
- Added libselinux-devel BuildPreqreq (#124283).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Phil Knirsch <pknirsch@redhat.com> 0.17-37
- rebuilt against latest procps lib.
- built stuff with PIE enabled.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 23 2004 Bill Nottingham <notting@redhat.com> 0.17-35
- rebuild against new libproc
- selinux is the default, remove the release suffix

* Tue Oct 21 2003 Dan Walsh <dwalsh@redhat.com> 0.17-34.sel
- remove -lattr

* Thu Oct 09 2003 Dan Walsh <dwalsh@redhat.com> 0.17-33.sel
- turn selinux on

* Fri Oct 03 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- rebuild

* Mon Sep 08 2003 Dan Walsh <dwalsh@redhat.com> 0.17-31.4
- turn selinux off

* Fri Sep 05 2003 Dan Walsh <dwalsh@redhat.com> 0.17-31.3.sel
- turn selinux on

* Mon Jul 28 2003 Dan Walsh <dwalsh@redhat.com> 0.17-31.2
- Add SELinux library support

* Mon Jul 14 2003 Tim Powers <timp@redhat.com> 0.17-31.1
- rebuilt for RHEL

* Mon Jul 07 2003 Elliot Lee <sopwith@redhat.com>
- Rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 23 2003 Tim Powers <timp@redhat.com> 0.17-29
- rebuilt

* Wed May 21 2003 Matt Wilson <msw@redhat.com> 0.17-28
- rebuilt

* Wed May 21 2003 Matt Wilson <msw@redhat.com> 0.17-27
- added netkit-rusers-0.17-rup-timeout.patch to fix immediate timeout
  problem in rup (#91322)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Phil Knirsch <pknirsch@redhat.com> 0.17-24
- Bumped release and rebuilt due to new procps.

* Mon Dec 02 2002 Elliot Lee <sopwith@redhat.com> 0.17-23
- Fix multilib

* Tue Nov  5 2002 Nalin Dahyabhai <nalin@redhat.com> 0.17-22
- Bumped release and rebuilt due to procps update.
- s/Copyright/License/g

* Thu Aug 08 2002 Phil Knirsch <pknirsch@redhat.com> 0.17-21
- Bumped release and rebuilt due to procps update.

* Wed Jul 17 2002 Phil Knirsch <pknirsch@redhat.com> 0.17-20
- Fixed the sort ordering for rup -l host1 host2 host3 (#67551)
- Don't use configure anymore, doesn't work in build environment correctly.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 0.17-19
- automated rebuild

* Wed Jun 19 2002 Phil Knirsch <pknirsch@redhat.com> 0.17-18
- Actually applied Matt's patch ;-)
- Don't forcibly strip binaries

* Mon Jun 10 2002 Matt Wilson <msw@redhat.com>
- fixed static buffer size which truncated /proc/stat when it was more
  than 1024 bytes (#64935)

* Tue Jun 04 2002 Phil Knirsch <pknirsch@redhat.com>
- bumped release number and rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 23 2002 Phil Knirsch <pknirsch@redhat.com>
- Fixed the wrong uptime problem introduced by fixing bug #53244.
- Fixed segfault problem on alpha (and other archs) (bug #53309).

* Thu Jan 17 2002 Phil Knirsch <pknirsch@redhat.com>
- Fixed bug #17065 where rusersd wrongly terminated each string with a '\0'.
- Fixed bug #53244. Now stats for the different protocols are stored separately.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jul 25 2001 Phil Knirsch <pknirsch@redhat.de>
- Fixed missing includes for time.h and several others (#49887)

* Wed Jun 27 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed rstatd.init script to use $0 in usage string (#26553)

* Wed Apr  4 2001 Jakub Jelinek <jakub@redhat.com>
- don't let configure to guess compiler, it can pick up egcs

* Wed Feb 14 2001 Nalin Dahyabhai <nalin@redhat.com>
- merge in Bob Matthews' patch, which solves other parts on 2.4 (#26447)

* Tue Feb  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- don't die if /proc/stat looks a little odd (#25519)

* Mon Feb  5 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- i18nize rstatd init script

* Tue Jan 24 2001 Nalin Dahyabhai <nalin@redhat.com>
- gettextize init script

* Sat Aug 05 2000 Bill Nottingham <notting@redhat.com>
- condrestart fixes

* Thu Jul 20 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Sun Jul 16 2000 Matt Wilson <msw@redhat.com>
- rebuilt against new procps

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Preston Brown <pbrown@redhat.com>
- move initscripts

* Sun Jun 18 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- update to 0.17.

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages (again).

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description and summary
- man pages are compressed

* Tue Jan  4 2000 Bill Nottingham <notting@redhat.com>
- split client and server

* Tue Dec 21 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.16.

* Wed Nov 10 1999 Bill Nottingham <notting@redhat.com>
- rebuild against new procps

* Wed Sep 22 1999 Jeff Johnson <jbj@redhat.com>
- rusers init script started rstatd.

* Mon Sep 20 1999 Jeff Johnson <jbj@redhat.com>
- (re-)initialize number of users (#5244).

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- initscripts check for portmapper running before starting (#2615)

* Fri Aug 27 1999 Jeff Johnson <jbj@redhat.com>
- return monitoring statistics like solaris does (#4237).

* Thu Aug 26 1999 Jeff Johnson <jbj@redhat.com>
- update to netkit-0.15.
- on startup, rpc.rstatd needs to read information twice (#3994).

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Tue Apr  6 1999 Jeff Johnson <jbj@redhat.com>
- add rpc.rstatd (#2000)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 22)

* Mon Mar 15 1999 Jeff Johnson <jbj@redhat.com>
- compile for 6.0.

* Tue May 05 1998 Cristian Gafton <gafton@redhat.com>
- added /etc/rc.d/init.d/functions to the init script

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- enhanced initscript

* Tue Oct 21 1997 Erik Troan <ewt@redhat.com>
- added init script
- users attr
- supports chkconfig

* Tue Jul 15 1997 Erik Troan <ewt@redhat.com>
- initial build
