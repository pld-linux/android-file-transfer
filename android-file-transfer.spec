# TODO
# - shared lib is not versioned
# - can't build shared and static in same build. drop shared bcond
#
# Conditional build:
%bcond_without	fuse		# Build fuse mount helper
%bcond_without	qt			# Build reference Qt application
%bcond_without	shared		# Build shared library
%bcond_with	static_libs	# don't build static libraries

# build doesn't support both
%if %{with shared}
%undefine static_libs
%endif

Summary:	Android File Transfer for Linux
Name:		android-file-transfer
Version:	3.4
Release:	0.1
License:	LGPLv2.1
Group:		X11/Applications
Source0:	https://github.com/whoozle/android-file-transfer-linux/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	691142fdbea216676df27bfc94885f71
URL:		https://whoozle.github.io/android-file-transfer-linux/
BuildRequires:	build-essential
BuildRequires:	cmake >= 2.8
%{?with_fuse:BuildRequires:	libfuse-devel}
BuildRequires:	libmagic-devel
BuildRequires:	libstdc++-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.727
%if %{with qt}
BuildRequires:	Qt5Widgets-devel
BuildRequires:	qt5-build
BuildRequires:	qt5-qmake
%endif
%if %{with shared}
Requires:	%{name}-libs = %{version}-%{release}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Android File Transfer for Linux - reliable MTP client with
minimalistic UI similar to Android File Transfer for Mac.

Features:
- Simple Qt UI with progress dialogs.
- FUSE wrapper (If you'd prefer mounting your device), supporting
  partial read/writes, allowing instant access to your files.
- No file size limits.
- Automatically renames album cover to make it visible from media
  player.
- USB 'Zerocopy' support found in recent Linux kernel (no user/kernel
  data copying)
- No extra dependencies (e.g. libptp/libmtp).
- Available as static/shared library.
- Command line tool (aft-mtp-cli)

%package libs
Summary:	Shared %{name} library
Group:		Libraries

%description libs
Shared %{name} library.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%package fuse
Summary:	aft-mtp-mount fuse wrapper
Group:		Applications
%if %{with shared}
Requires:	%{name}-libs = %{version}-%{release}
%endif

%description fuse
FUSE wrapper (If you'd prefer mounting your device), supporting
partial read/writes, allowing instant access to your files.

%package qt
Summary:	Qt GUI
Group:		X11/Applications
%if %{with shared}
Requires:	%{name}-libs = %{version}-%{release}
%endif

%description qt
Qt GUI.

%prep
%setup -q -n %{name}-linux-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	-DBUILD_FUSE=%{!?with_fuse:OFF}%{?with_fuse:ON} \
	-DBUILD_QT_UI=%{!?with_qt:OFF}%{?with_qt:ON} \
	-DBUILD_SHARED_LIB=%{!?with_shared:OFF}%{?with_shared:ON} \
	..
%ninja_build

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aft-mtp-cli

%if %{with fuse}
%files fuse
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aft-mtp-mount
%endif

%if %{with qt}
%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/android-file-transfer
%{_desktopdir}/android-file-transfer.desktop
%{_iconsdir}/hicolor/512x512/apps/android-file-transfer.png
%{_datadir}/metainfo/android-file-transfer.appdata.xml
%endif

%if %{with shared}
%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmtp-ng.so
%endif

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmtp-ng-static.a
%endif
