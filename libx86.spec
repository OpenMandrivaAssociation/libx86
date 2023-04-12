%define major	1
%define libname	%mklibname x86 %{major}
%define devname	%mklibname x86 -d

Summary:	Hardware-independent library for executing real-mode x86 code
Name:		libx86
Version:	1.1
Release:	26
Group:		System/Libraries
License:	MIT
Url:		http://www.codon.org.uk/~mjg59/libx86/
Source0:	http://www.codon.org.uk/~mjg59/libx86/downloads/%{name}-%{version}.tar.gz
Patch0:		https://src.fedoraproject.org/rpms/libx86/raw/rawhide/f/libx86-add-pkgconfig.patch
Patch1:		https://src.fedoraproject.org/rpms/libx86/raw/rawhide/f/libx86-mmap-offset.patch
# patch from  https://bugs.debian.org/cgi-bin/bugreport.cgi?msg=34;filename=libx86-libc-test.patch.txt;att=1;bug=570676
# debian control portion removed as it fails to apply and we do not need it anyway
Patch2:		https://src.fedoraproject.org/rpms/libx86/raw/rawhide/f/libx86-libc-test.patch
Patch3:		https://src.fedoraproject.org/rpms/libx86/raw/rawhide/f/libx86-fix_processor_flags.patch
Patch4:		https://src.fedoraproject.org/rpms/libx86/raw/rawhide/f/libx86-ld_flags.patch
# does not build on ppc, ppc64 and s390* yet, due to the lack of port i/o
# redirection and video routing
ExcludeArch:    ppc ppc64 s390 s390x %{sparcx} %{armx}

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
%autosetup -p1

%build
%set_build_flags
%make_build BACKEND=x86emu CFLAGS="%{optflags} -fPIC"

%install
%make_install LIBDIR=%{_libdir}
chmod 0644 %{buildroot}%{_libdir}/libx86.a

%files -n %{libname}
%{_libdir}/libx86.so.%{major}

%files -n %{devname}
%doc COPYRIGHT
%{_libdir}/libx86.a
%{_libdir}/libx86.so
%{_includedir}/libx86.h
%{_libdir}/pkgconfig/x86.pc
