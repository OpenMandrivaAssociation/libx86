%define major	1
%define libname	%mklibname x86 %{nil} %{major}
%define develname	%mklibname x86 -d

%bcond_without	uclibc

Name:		libx86
Version:	1.1
Release:	%mkrel 9
Summary:	Hardware-independent library for executing real-mode x86 code
Group:		System/Libraries
URL:		http://www.codon.org.uk/~mjg59/libx86/
Source:		http://www.codon.org.uk/~mjg59/libx86/downloads/%{name}-%{version}.tar.gz
Patch0:		libx86-0.99-ifmask.patch
License:	MIT
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
ExclusiveArch:	%{ix86} x86_64
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif

%description
It's often useful to be able to make real-mode x86 BIOS calls from userland.
lrmi provides a simple interface to this for x86 machines, but this doesn't
help on other platforms.

libx86 provides the lrmi interface, but will also run on platforms such as
amd64 and alpha.

%package -n	%{libname}
Summary:	Hardware-independent library for executing real-mode x86 code
Group:		System/Libraries

%description -n	%{libname}
It's often useful to be able to make real-mode x86 BIOS calls from userland.
lrmi provides a simple interface to this for x86 machines, but this doesn't
help on other platforms.

libx86 provides the lrmi interface, but will also run on platforms such as
amd64 and alpha.

This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
This package contains the development files for %{name}.

%prep
%setup -q
%patch0 -p0

%build
%if %{with uclibc}
%ifarch %ix86
%make CC=%{uclibc_cc} CFLAGS="%{uclibc_cflags}" static
%else
%make CC=%{uclibc_cc} BACKEND=x86emu CFLAGS="%{uclibc_cflags} -fPIC" static
%endif
mkdir -p uclibc
mv -f libx86.a uclibc/libx86.a
make clean
%endif

%ifarch %ix86
%make CFLAGS="%{optflags}"
%else
%make BACKEND=x86emu CFLAGS="%{optflags} -fPIC"
%endif

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} LIBDIR=%{_libdir} install
chmod 0644 %{buildroot}%{_libdir}/libx86.a
%if %{with uclibc}
install -m644 uclibc/libx86.a -D %{buildroot}%{uclibc_root}%{_libdir}/libx86.a
%endif

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%doc COPYRIGHT
%{_libdir}/libx86.so.%{major}

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/libx86.a
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libx86.a
%endif
%{_libdir}/libx86.so
%{_includedir}/libx86.h



%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1-9mdv2011.0
+ Revision: 661556
- mass rebuild

* Sun Nov 28 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1-8mdv2011.0
+ Revision: 602618
- rebuild

* Sat Dec 05 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.1-7mdv2010.1
+ Revision: 473683
- cosmetics...
- correct license tag
- build uclibc linked static library

* Sun Sep 27 2009 Olivier Blin <oblin@mandriva.com> 1.1-6mdv2010.0
+ Revision: 450113
- build on x86_64 too
- build on ix86 only (from Arnaud Patard)

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.1-5mdv2010.0
+ Revision: 425881
- rebuild

* Fri Apr 10 2009 Funda Wang <fwang@mandriva.org> 1.1-4mdv2009.1
+ Revision: 365805
- use fpic
- fix ifmask (patch from gentoo)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon May 19 2008 Pascal Terjan <pterjan@mandriva.org> 1.1-2mdv2009.0
+ Revision: 209214
- Fix make install on x86_64
- Update to 1.1

* Mon May 19 2008 Pascal Terjan <pterjan@mandriva.org> 1.0-2mdv2009.0
+ Revision: 208851
- Fix build on non x86
- First version of the package


