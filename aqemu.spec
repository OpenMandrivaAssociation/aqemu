Name:		aqemu
Version:	0.9.4
Release:	1
Summary:	A QT graphical interface to QEMU and KVM
Group:		Emulators
License:	GPLv2+
# Originally:
# URL:		http://aqemu.sourceforge.net
# Source0:	https://github.com/tobimensch/aqemu/archive/v%{version}.tar.gz
# Also quite dead, but at least marginally newer fork:
Source0:	https://github.com/TBK/aqemu/archive/refs/tags/v%{version}.tar.gz
Patch0:		aqemu-0.9.4-missing-includes.patch

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	desktop-file-utils
BuildRequires:	qt5-devel
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5DBus)
BuildRequires:	cmake(Qt5Network)
BuildRequires:	cmake(Qt5PrintSupport)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	cmake(Qt5Test)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(libvncserver)

Requires: qemu

%files
%{_bindir}/%{name}
%doc AUTHORS CHANGELOG COPYING TODO
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/aqemu.appdata.xml
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_mandir}/man1/%{name}.1*

#---------------------------------------------------------------------------

%description
AQEMU is a graphical user interface to QEMU and KVM, written in Qt4. The
program has a user-friendly interface and allows user to set the
majority of QEMU and KVM options on their virtual machines.

%prep
%autosetup -p1

%build
export PATH=%{_qt5_bindir}:$PATH
%cmake \
	-DWITHOUT_EMBEDDED_DISPLAY:BOOL=OFF \
	-DUPDATE_TRANSLATIONS_BOOL=OFF \
	-DINSTALL_MAN:BOOL=ON \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# Copy 48x48 and 64x64 icons to correct location.
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{48x48,64x64}/apps
mv %{buildroot}%{_datadir}/pixmaps/%{name}_48x48.png \
   %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
mv %{buildroot}%{_datadir}/pixmaps/%{name}.png \
   %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png

# Remove directories from install which are not being deployed in RPM.
rm -rf %{buildroot}%{_datadir}/pixmaps
rm -rf %{buildroot}%{_datadir}/menu
rm -rf %{buildroot}%{_datadir}/doc/%{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
