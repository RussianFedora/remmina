Name:           remmina
Version:        0.9.3
Release:        5%{?dist}.R
Summary:        Remote Desktop Client

Group:          Applications/Internet
License:        GPLv2+ and MIT
URL:            http://remmina.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel
BuildRequires:  libssh-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  avahi-ui-devel
BuildRequires:  vte-devel
BuildRequires:  unique-devel
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  desktop-file-utils      

# Remmina used to be called grdc
Provides:       grdc = %{version}
Obsoletes:      grdc < 0.6.1

# Remmina has a generic trayicon now
Provides:       gnome-applet-remmina = %{version}
Provides:       xfce4-remmina-plugin = %{version}
Obsoletes:      gnome-applet-remmina <= 0.7.3
Obsoletes:      xfce4-remmina-plugin <= 0.7.3


%description
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

Remmina supports multiple network protocols in an integrated and consistent
user interface. Currently RDP, VNC, XDMCP and SSH are supported.

Please don't forget to install the plugins for the protocols you want to use.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains header files for developing plugins for 
%{name}.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor="" --delete-original \
  --add-category="RemoteAccess" \
  --remove-category="X-GNOME-NetworkSettings" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  $RPM_BUILD_ROOT/%{_datadir}/applications/%{name}.desktop

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README 
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/%{name}/

%files devel
%defattr(-,root,root,-)
%doc
%{_includedir}/%{name}/

%changelog
* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.9.3-4
- Rebuild for new libpng

* Sat Mar 05 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.3-3
- Fix obsoletes for for gnome-applet-remmina and xfce4-remmina-plugin

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.3-1
- Update to 0.9.3

* Sun Nov 28 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.3-1
- Update to 0.8.3
- Plugins are in remmina-plugins now

* Sat Nov 27 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.7.5-3
- Enable 32-bit color depth (#656120)

* Mon Jul 19 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.7.5-2
- Fix menu entry (#616115)

* Wed May 05 2010 Damien Durand <splinux@fedoraproject.org> - 0.7.5-1
- Upstream release, 0.7.5
- Remove the old "DSO" patch

* Tue Mar 16 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.7.4-2
- Add patch to fix DSO issue

* Sat Feb 27 2010 Damien Durand <splinux@fedoraproject.org> 0.7.4-1
- Update to 0.7.4
- Fix License tag

* Sun Feb 14 2010 Damien Durand <splinux@fedoraproject.org> 0.7.3-1
- Upstream release
- Add rdesktop, xorg-x11-server-Xephyr in Requires
- Add grdc in Provides/Obsoletes
- Add --enable-vnc=dl in %%configure
- Remove unneeded README.LibVNCServer
- Fix "icons/hicolor" path

* Thu Jan 07 2010 Damien Durand <splinux@fedoraproject.org> 0.7.2-2
- Fix Summary
- Split BuildRequires

* Thu Jan 07 2010 Damien Durand <splinux@fedoraproject.org> 0.7.2-1
- Initial release
