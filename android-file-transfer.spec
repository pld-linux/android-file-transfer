# TODO
# - BUILD_QT_UI off bcond
# - subpackages
Summary:	Android File Transfer for Linux
Name:		android-file-transfer
Version:	3.4
Release:	0.1
License:	LGPLv2.1
Group:		X11/Applications
Source0:	https://github.com/whoozle/android-file-transfer-linux/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	691142fdbea216676df27bfc94885f71
URL:		https://whoozle.github.io/android-file-transfer-linux/
BuildRequires:	Qt5Widgets-devel
BuildRequires:	build-essential
BuildRequires:	cmake
BuildRequires:	libfuse-devel
BuildRequires:	libstdc++-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt5-build
BuildRequires:	qt5-qmake
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.727
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

%prep
%setup -q -n %{name}-linux-%{version}

%build
install -d build
cd build
%cmake -G Ninja ..
%ninja_build

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aft-mtp-cli
%attr(755,root,root) %{_bindir}/aft-mtp-mount
%attr(755,root,root) %{_bindir}/android-file-transfer
%{_libdir}/libmtp-ng-static.a
%{_desktopdir}/android-file-transfer.desktop
%{_iconsdir}/hicolor/512x512/apps/android-file-transfer.png
%{_datadir}/metainfo/android-file-transfer.appdata.xml
