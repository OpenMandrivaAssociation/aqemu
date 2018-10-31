%define	debug_package	%nil

Name:		aqemu
Version:	0.9.2
Release:	2
Summary:	A QT graphical interface to QEMU and KVM
Group:		Emulators
License:	GPLv2+
URL:		http://aqemu.sourceforge.net
Source0:	https://github.com/tobimensch/aqemu/archive/v%{version}.tar.gz
Patch0:		aqemu-0.9.2-qtbindir.patch
BuildRequires:	qt5-devel
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5PrintSupport)
BuildRequires:	cmake(Qt5Test)
BuildRequires:	cmake(Qt5DBus)
BuildRequires:	cmake
BuildRequires:	pkgconfig(libvncserver)
BuildRequires:	desktop-file-utils
BuildRequires:	gnutls-devel

Requires: qemu

%description
AQEMU is a graphical user interface to QEMU and KVM, written in Qt4. The
program has a user-friendly interface and allows user to set the
majority of QEMU and KVM options on their virtual machines.

%prep
%setup -q
%apply_patches

%build
%cmake
%make

%install
%makeinstall_std -C build
# Copy 48x48 and 64x64 icons to correct location.
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{48x48,64x64}/apps
mv %{buildroot}%{_datadir}/pixmaps/%{name}_48x48.png \
   %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
mv %{buildroot}%{_datadir}/pixmaps/%{name}_64x64.png \
   %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
# Remove directories from install which are not being deployed in RPM.
rm -rf %{buildroot}%{_datadir}/pixmaps
rm -rf %{buildroot}%{_datadir}/menu
rm -rf %{buildroot}%{_datadir}/doc/%{name}
# Validate the icon file.
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%{_bindir}/%{name}
%doc AUTHORS CHANGELOG COPYING TODO
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_mandir}/man1/%{name}.1*
