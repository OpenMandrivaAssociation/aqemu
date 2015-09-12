%define	debug_package	%nil

Name:		aqemu
Version:	0.8.2
Release:	10
Summary:	A QT graphical interface to QEMU and KVM
Group:		Emulators
License:	GPLv2+
URL:		http://aqemu.sourceforge.net
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
# Patch for desktop file to ensure it shows up in the GNOME overview.
# Upstream: http://sourceforge.net/tracker/?func=detail&aid=3430317&group_id=229794&atid=1078458
Patch0:		aqemu-0.8.2-rosa-desktop.patch
# Fatch for vncview.cp file to disable macro that clashes with QT 4.8.
# Upstram: http://sourceforge.net/tracker/?func=detail&aid=3429937&group_id=229794&atid=1078458
Patch1:		aqemu-0.8.2-qt48.patch
Patch2:		Utils-format-path.patch
BuildRequires:	qt-devel 
BuildRequires:	cmake 
BuildRequires:	pkgconfig(libvncserver)
BuildRequires:	desktop-file-utils
BuildRequires:	gnutls-devel
BuildRequires: 	hicolor-icon-theme
BuildRequires:	gcc-c++, gcc, gcc-cpp

Requires: qemu

%description
AQEMU is a graphical user interface to QEMU and KVM, written in Qt4. The 
program has a user-friendly interface and allows user to set the 
majority of QEMU and KVM options on their virtual machines.

%prep
%setup -q
%patch0
%patch1
%patch2 -p1

%build
export CC=gcc
export CXX=g++

cmake -DCMAKE_INSTALL_PREFIX=/usr -DMAN_PAGE_COMPRESSOR=bzip2
#cmake
%make

%install
%makeinstall_std
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

