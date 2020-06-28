Name:		crun
Summary:	OCI Container Runtime fully written in C
Version:	0.3
Release:	1
Source0:	https://github.com/containers/crun/archive/v0.3/%{name}-%{version}.tar.gz
# Those are pulled in with "git submodule" in upstream git
Source1:	https://github.com/giuseppe/libocispec/archive/8302d573323e7c7af0850cb37d63ad3bfb9637b8.tar.gz
Source2:	https://github.com/opencontainers/image-spec/archive/09950c5fb1bb6745e72aa26ecde0d540e35f5286.tar.gz
Source3:	https://github.com/opencontainers/runtime-spec/archive/31e0d16c1cb7967f2ec8843472874da7accf2202.tar.gz
Group:		Servers
License:	GPLv3+/LGPLv3+
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	make
BuildRequires:	pkgconfig(yajl)
BuildRequires:	pkgconfig(libseccomp)
BuildRequires:	pkgconfig(libselinux)
BuildRequires:	pkgconfig(libcap)
BuildRequires:	pkgconfig(libsystemd)

%description
A fast and low-memory footprint OCI Container Runtime fully written in C.

crun conforms to the OCI Container Runtime specifications
(https://github.com/opencontainers/runtime-spec).

%prep
%autosetup -p1 -a 1
rmdir libocispec
mv libocispec-* libocispec
cd libocispec
rmdir image-spec runtime-spec
tar xf %{S:2}
tar xf %{S:3}
mv image-spec-* image-spec
mv runtime-spec-* runtime-spec
cd ..
autoreconf -fis
%configure

%build
%make_build

%install
%make_install
# No point in shipping a static library if the headers
# aren't installed...
rm %{buildroot}%{_libdir}/*.a

%files
%{_bindir}/crun
