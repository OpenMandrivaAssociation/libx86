%define major	1
%define libname	%mklibname x86 %{major}
%define devname	%mklibname x86 -d

Summary:	Hardware-independent library for executing real-mode x86 code
Name:		libx86
Version:	1.1
Release:	25
Group:		System/Libraries
License:	MIT
Url:		http://www.codon.org.uk/~mjg59/libx86/
Source0:	http://www.codon.org.uk/~mjg59/libx86/downloads/%{name}-%{version}.tar.gz
Patch0:		libx86-0.99-ifmask.patch
# (RH/Dave Airlie):
Patch1:		libx86-add-pkgconfig.patch
# does not build on ppc, ppc64 and s390* yet, due to the lack of port i/o
# redirection and video routing
ExcludeArch:    ppc ppc64 s390 s390x %{sparcx}

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

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the development files for %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p1

%build
%ifarch %{ix86}
%make CFLAGS="%{optflags}"
%else
%make BACKEND=x86emu CFLAGS="%{optflags} -fPIC"
%endif

%install
%makeinstall_std LIBDIR=%{_libdir}
chmod 0644 %{buildroot}%{_libdir}/libx86.a

%files -n %{libname}
%{_libdir}/libx86.so.%{major}

%files -n %{devname}
%doc COPYRIGHT
%{_libdir}/libx86.a
%{_libdir}/libx86.so
%{_includedir}/libx86.h
%{_libdir}/pkgconfig/x86.pc
