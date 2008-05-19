%define name	libx86
%define version	1.1
%define release	%mkrel 1
%define major	1
%define libname	%mklibname x86 %{nil} %{major}
%define develname	%mklibname x86 -d

Name:		%name
Version:	%version
Release:	%release
Summary:	Hardware-independent library for executing real-mode x86 code
Group:		System/Libraries
URL:		http://www.codon.org.uk/~mjg59/libx86/
Source:		http://www.codon.org.uk/~mjg59/libx86/downloads/%{name}-%{version}.tar.gz
License:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
It's often useful to be able to make real-mode x86 BIOS calls from userland.
lrmi provides a simple interface to this for x86 machines, but this doesn't
help on other platforms.

libx86 provides the lrmi interface, but will also run on platforms such as
amd64 and alpha.

%package -n %{libname}
Summary:	Hardware-independent library for executing real-mode x86 code
Group:		System/Libraries

%description -n %{libname}
It's often useful to be able to make real-mode x86 BIOS calls from userland.
lrmi provides a simple interface to this for x86 machines, but this doesn't
help on other platforms.

libx86 provides the lrmi interface, but will also run on platforms such as
amd64 and alpha.

This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains the development files for %{name}.

%prep
%setup -q

%build
%ifarch %ix86
%make
%else
%make BACKEND=x86emu
%endif

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} LIBDIR=%{_libdir} install
chmod 0644 %{buildroot}%{_libdir}/libx86.a

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%doc COPYRIGHT
%{_libdir}/libx86.so.%{major}

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/libx86.a
%{_libdir}/libx86.so
%{_includedir}/libx86.h

