# Copyright (c) 2002-2005, Network Appliance, Inc. All rights reserved.
# Copyright (c) 2007-2015, Intel Corporation. All rights reserved.
#
# This Software is licensed under one of the following licenses:
#
# 1) under the terms of the "Common Public License 1.0" a copy of which is
#    in the file LICENSE.txt in the root directory. The license is also
#    available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/cpl.php.
#
# 2) under the terms of the "The BSD License" a copy of which is in the file
#    LICENSE2.txt in the root directory. The license is also available from
#    the Open Source Initiative, see
#    http://www.opensource.org/licenses/bsd-license.php.
#
# 3) under the terms of the "GNU General Public License (GPL) Version 2" a 
#    copy of which is in the file LICENSE3.txt in the root directory. The 
#    license is also available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/gpl-license.php.
#
# Licensee has the right to choose one of the above licenses.
#
# Redistributions of source code must retain the above copyright
# notice and one of the license notices.
#
# Redistributions in binary form must reproduce both the above copyright
# notice, one of the license notices in the documentation
# and/or other materials provided with the distribution.
#
#
# uDAT and uDAPL 2.0 Registry RPM SPEC file
#
# $Id: $

Name: dapl
Version: 2.1.10
Release: 2%{?dist}
Summary: A Library for userspace access to RDMA devices using OS Agnostic DAT APIs, proxy daemon for offloading RDMA 

Group: System Environment/Libraries
License: Dual GPL/BSD/CPL
Url: http://openfabrics.org/
Source: http://www.openfabrics.org/downloads/%{name}/%{name}-%{version}.tar.gz
BuildRoot: %{_topdir}/BUILDROOT
Obsoletes: intel-mic-ofed-dapl
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig

%description
Along with the OpenFabrics kernel drivers, libdat and libdapl provides a userspace
RDMA API that supports DAT 2.0 specification and IB transport extensions for
atomic operations and rdma write with immediate data.

%package devel
Summary: Development files for the libdat and libdapl libraries
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: intel-mic-ofed-dapl-devel

%description devel
Header files for libdat and libdapl library.

%package devel-static
Summary: Static development files for libdat and libdapl library
Group: System Environment/Libraries
Obsoletes: intel-mic-ofed-dapl-devel-static
 
%description devel-static
Static libraries for libdat and libdapl library.

%package utils
Summary: Test suites for uDAPL library
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Obsoletes: intel-mic-ofed-dapl-utils

%description utils
Useful test suites to validate uDAPL library API's.

%prep
%setup -q

%build
%configure

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_libdir}/*.la

# make init.d so we can exclude it later:
mkdir -p %{buildroot}%{_sysconfdir}/init.d
touch mcm-files

%clean
rm -rf %{buildroot}

%post
# fix problem with older dapl packages that clobber dat.conf when updating
cp %{_sysconfdir}/dat.conf /tmp/%{version}-dat.conf
/sbin/ldconfig

if [ $1 -gt 1 ]; then
	/sbin/chkconfig --add mpxyd &> /dev/null || true
	service mpxyd start
elif [ $1 -gt 2 ]; then
	service mpxyd restart
fi

%preun
if [ -f /etc/init.d/mpxyd ]; then
	/sbin/chkconfig --del mpxyd &> /dev/null
	service mpxyd stop
fi

%postun 
/sbin/ldconfig

%files -f mcm-files
%defattr(-,root,root,-)
%{_libdir}/libda*.so.*
%config %{_sysconfdir}/dat.conf
%doc AUTHORS README COPYING ChangeLog LICENSE.txt LICENSE2.txt LICENSE3.txt README.mcm

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%dir %{_includedir}/dat2
%{_includedir}/dat2/*

%files devel-static
%defattr(-,root,root,-)
%{_libdir}/*.a

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*

%triggerpostun -- dapl < 2.0.35-1
# fix problem with older dapl packages that clobber dat.conf during update
mv /tmp/%{version}-dat.conf %{_sysconfdir}/dat.conf

%changelog
* Wed Dec 14 2016 Arlin Davis <ardavis@ichips.intel.com> - 2.1.10
- DAT/DAPL Version 2.1.10 Release 1, OFED 4.8, MPSS 3.8, MPSS 4.4 

* Fri Apr 29 2016 Arlin Davis <ardavis@ichips.intel.com> - 2.1.9
- DAT/DAPL Version 2.1.9 Release 2, OFED 3.18-2 GA, MPSS 3.7.1 

* Thu Apr 14 2016 Arlin Davis <ardavis@ichips.intel.com> - 2.1.9
- DAT/DAPL Version 2.1.9 Release 1, OFED 3.18-2 GA, MPSS 3.7 

* Tue Feb 16 2016 Arlin Davis <ardavis@ichips.intel.com> - 2.1.8
- DAT/DAPL Version 2.1.8 Release 1, OFED 3.18-2, MPSS 3.7 

* Tue Sep 29 2015 Arlin Davis <ardavis@ichips.intel.com> - 2.1.7
- DAT/DAPL Version 2.1.7 Release 1, OFED 3.18-1 GA

* Wed Aug 12 2015 Arlin Davis <ardavis@ichips.intel.com> - 2.1.6
- DAT/DAPL Version 2.1.6 Release 1, OFED 3.18-1

* Mon May 26 2015 Arlin Davis <ardavis@ichips.intel.com> - 2.1.5
- DAT/DAPL Version 2.1.5 Release 1, OFED 3.18

* Thu Mar 19 2015 Arlin Davis <ardavis@ichips.intel.com> - 2.1.4
- DAT/DAPL Version 2.1.4 Release 1, OFED 3.18

* Mon Dec 15 2014 Arlin Davis <ardavis@ichips.intel.com> - 2.1.3
- DAT/DAPL Version 2.1.3 Release 1, OFED 3.18 RC

* Tue Sep 2 2014 Arlin Davis <ardavis@ichips.intel.com> - 2.1.2
- DAT/DAPL Version 2.1.2 Release 1, OFED 3.12-1

* Wed Aug 13 2014 Arlin Davis <ardavis@ichips.intel.com> - 2.1.1
- DAT/DAPL Version 2.1.1 Release 1, OFED 3.12-1

* Fri Jul 18 2014 Arlin Davis <ardavis@ichips.intel.com> - 2.1.0
- DAT/DAPL Version 2.1.0 Release 1, add MIC support, OFED 3.12-1

* Sun May 4 2014 Arlin Davis <ardavis@ichips.intel.com> - 2.0.42
- DAT/DAPL Version 2.0.42 Release 1, OFED 3.12 GA

* Fri Mar 14 2014 Arlin Davis <ardavis@ichips.intel.com> - 2.0.41
- DAT/DAPL Version 2.0.41 Release 1, OFED 3.12 GA

* Mon Feb 10 2014 Arlin Davis <ardavis@ichips.intel.com> - 2.0.40
- DAT/DAPL Version 2.0.40 Release 1, OFED 3.12

* Thu Oct 3 2013 Arlin Davis <ardavis@ichips.intel.com> - 2.0.39
- DAT/DAPL Version 2.0.39 Release 1, OFED 3.5-2 

* Mon Jul 22 2013 Arlin Davis <ardavis@ichips.intel.com> - 2.0.38
- DAT/DAPL Version 2.0.38 Release 1, OFED 3.5.2 

* Thu Jun 6 2013 Arlin Davis <ardavis@ichips.intel.com> - 2.0.37
- DAT/DAPL Version 2.0.37 Release 1, OFED 3.5.2 

* Sun Aug 5 2012 Arlin Davis <ardavis@ichips.intel.com> - 2.0.36
- DAT/DAPL Version 2.0.36 Release 1, OFED 3.x 

* Mon Apr 23 2012 Arlin Davis <ardavis@ichips.intel.com> - 2.0.35
- DAT/DAPL Version 2.0.35 Release 1, OFED 3.2  

* Wed Nov 2 2011 Arlin Davis <ardavis@ichips.intel.com> - 2.0.34
- DAT/DAPL Version 2.0.34 Release 1, OFED 1.5.4 GA

* Mon Aug 29 2011 Arlin Davis <ardavis@ichips.intel.com> - 2.0.33
- DAT/DAPL Version 2.0.33 Release 1, OFED 1.5.4 RC1 

* Sun Feb 13 2011 Arlin Davis <ardavis@ichips.intel.com> - 2.0.32
- DAT/DAPL Version 2.0.32 Release 1, OFED 1.5.3 GA 

* Fri Dec 10 2010 Arlin Davis <ardavis@ichips.intel.com> - 2.0.31
- DAT/DAPL Version 2.0.31 Release 1, OFED 1.5.3  

* Mon Aug 9 2010 Arlin Davis <ardavis@ichips.intel.com> - 2.0.30
- DAT/DAPL Version 2.0.30 Release 1, OFED 1.5.2 RC4 

* Thu Jun 17 2010 Arlin Davis <ardavis@ichips.intel.com> - 2.0.29
- DAT/DAPL Version 2.0.29 Release 1, OFED 1.5.2 RC2 

* Mon May 24 2010 Arlin Davis <ardavis@ichips.intel.com> - 2.0.28
- DAT/DAPL Version 2.0.28 Release 1, OFED 1.5.2 RC1 

* Tue Feb 23 2010 Arlin Davis <ardavis@ichips.intel.com> - 2.0.27
- DAT/DAPL Version 2.0.27 Release 1, OFED 1.5.1  

* Mon Jan 11 2010 Arlin Davis <ardavis@ichips.intel.com> - 2.0.26
- DAT/DAPL Version 2.0.26 Release 1, OFED 1.5, OFED 1.5-RDMAoE  

* Tue Nov 24 2009 Arlin Davis <ardavis@ichips.intel.com> - 2.0.25
- DAT/DAPL Version 2.0.25 Release 1, OFED 1.5 RC3 

* Fri Oct 30 2009 Arlin Davis <ardavis@ichips.intel.com> - 2.0.24
- DAT/DAPL Version 2.0.24 Release 1, OFED 1.5 RC2 

* Fri Oct 2 2009 Arlin Davis <ardavis@ichips.intel.com> - 2.0.23
- DAT/DAPL Version 2.0.23 Release 1, OFED 1.5 RC1 

* Wed Aug 19 2009 Arlin Davis <ardavis@ichips.intel.com> - 2.0.22
- DAT/DAPL Version 2.0.22 Release 1, OFED 1.5 ALPHA new UCM provider 

* Wed Aug 5 2009 Arlin Davis <ardavis@ichips.intel.com> - 2.0.21
- DAT/DAPL Version 2.0.21 Release 1, WinOF 2.1, OFED 1.4.1+  

* Fri Jun 19 2009 Arlin Davis <ardavis@ichips.intel.com> - 2.0.20
- DAT/DAPL Version 2.0.20 Release 1, OFED 1.4.1 + UD reject/scaling fixes 

* Thu Apr 30 2009 Arlin Davis <ardavis@ichips.intel.com> - 2.0.19
- DAT/DAPL Version 2.0.19 Release 1, OFED 1.4.1 GA Final 

* Fri Apr 17 2009 Arlin Davis <ardavis@ichips.intel.com> - 2.0.18
- DAT/DAPL Version 2.0.18 Release 1, OFED 1.4.1 GA 

* Tue Mar 31 2009 Arlin Davis <ardavis@ichips.intel.com> - 2.0.17
- DAT/DAPL Version 2.0.17 Release 1, OFED 1.4.1 GA

* Mon Mar 16 2009 Arlin Davis <ardavis@ichips.intel.com> - 2.0.16
- DAT/DAPL Version 2.0.16 Release 1, OFED 1.4.1 

* Fri Nov 07 2008 Arlin Davis <ardavis@ichips.intel.com> - 2.0.15
- DAT/DAPL Version 2.0.15 Release 1, OFED 1.4 GA

* Fri Oct 03 2008 Arlin Davis <ardavis@ichips.intel.com> - 2.0.14
- DAT/DAPL Version 2.0.14 Release 1, OFED 1.4 rc3

* Mon Sep 01 2008 Arlin Davis <ardavis@ichips.intel.com> - 2.0.13
- DAT/DAPL Version 2.0.13 Release 1, OFED 1.4 rc1

* Thu Aug 21 2008 Arlin Davis <ardavis@ichips.intel.com> - 2.0.12
- DAT/DAPL Version 2.0.12 Release 1, OFED 1.4 beta

* Sun Jul 20 2008 Arlin Davis <ardavis@ichips.intel.com> - 2.0.11
- DAT/DAPL Version 2.0.11 Release 1, IB UD extensions in SCM provider 

* Mon Jun 23 2008 Arlin Davis <ardavis@ichips.intel.com> - 2.0.10
- DAT/DAPL Version 2.0.10 Release 1, socket CM provider 

* Tue May 20 2008 Arlin Davis <ardavis@ichips.intel.com> - 2.0.9
- DAT/DAPL Version 2.0.9 Release 1, OFED 1.3.1 GA  

* Thu May 1 2008 Arlin Davis <ardavis@ichips.intel.com> - 2.0.8
- DAT/DAPL Version 2.0.8 Release 1, OFED 1.3.1  

* Thu Feb 14 2008 Arlin Davis <ardavis@ichips.intel.com> - 2.0.7
- DAT/DAPL Version 2.0.7 Release 1, OFED 1.3 GA 

* Mon Feb 04 2008 Arlin Davis <ardavis@ichips.intel.com> - 2.0.6
- DAT/DAPL Version 2.0.6 Release 1, OFED 1.3 RC4

* Tue Jan 29 2008 Arlin Davis <ardavis@ichips.intel.com> - 2.0.5
- DAT/DAPL Version 2.0.5 Release 1, OFED 1.3 RC3

* Thu Jan 17 2008 Arlin Davis <ardavis@ichips.intel.com> - 2.0.4
- DAT/DAPL Version 2.0.4 Release 1, OFED 1.3 RC2

* Tue Nov 20 2007 Arlin Davis <ardavis@ichips.intel.com> - 2.0.3
- DAT/DAPL Version 2.0.3 Release 1

* Tue Oct 30 2007 Arlin Davis <ardavis@ichips.intel.com> - 2.0.2
- DAT/DAPL Version 2.0.2 Release 1

* Tue Sep 18 2007 Arlin Davis <ardavis@ichips.intel.com> - 2.0.1-1
- OFED 1.3-alpha, co-exist with DAT 1.2 library package.  

* Wed Mar 7 2007 Arlin Davis <ardavis@ichips.intel.com> - 2.0.0.pre
- Initial release of DAT 2.0 APIs, includes IB extensions 
