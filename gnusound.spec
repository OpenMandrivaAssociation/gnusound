%define name 	gnusound
%define version 0.7.4
%define release %mkrel 6
%define Summary Multitrack sound editor for GNOME

Summary: 	%{Summary}
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	ftp://ftp.gnu.org/gnu/gnusound/%{name}-%{version}.tar.bz2
Patch0:     	%{name}-destdir.patch
Patch1:     gnusound-ffmpeg-struct.patch
Patch2:     gnusound-non-x86.patch
Patch3:		gnusound-autoconf.patch
Patch4: 	gnusound-ffmpeg-new-location.patch
Patch5:		gnusound-0.7.4-gtk212.patch
License: 	GPL
Group: 		Sound
Url: 		http://www.gnu.org/software/gnusound/index.orig.html
BuildRoot: 	%{_tmppath}/%{name}-buildroot
BuildRequires: 	libglade2.0-devel
BuildRequires: 	libgnomeui2-devel
BuildRequires:	libalsa-devel libsamplerate-devel
BuildRequires:	libaudiofile-devel libsndfile-devel
BuildRequires:	libflac-devel jackit-devel
BuildRequires:	libogg-devel libvorbis-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	ImageMagick

# This software sucks
# I add this for now to make it works
# but there is an overflow to fix !
%define _fortify_cflags %nil

%description
A gnu sound editor

%prep
%setup -q 
%patch0 -p1
%patch1 -p0 -b .ffmpeg-struct
%patch2 -p0 -b .non-x86
%patch3 -p0 -b .autoconf
%patch4 -p0
%patch5 -p1
%build

aclocal -I config
libtoolize --force
autoconf || :

%ifnarch i686 k6 athlon p3 p4
cat src/config.h |\
sed 's|define USE_FLOAT_TO_INT_METHOD .|define USE_FLOAT_TO_INT_METHOD 2|' |\
sed 's|define USE_MMX_MINMAX .|define USE_MMX_MINMAX 0|' |\
sed 's|define ARCH_X86|undef ARCH_X86|' \
> src/config.h.new
cp -f src/config.h.new src/config.h
%endif

%configure2_5x --with-gnome2 
%make

%install
%makeinstall_std

(
cd $RPM_BUILD_ROOT/%_libdir/gnusound/modules/
for i in *.so; do
    strip $i || true
done
)

mkdir -p $RPM_BUILD_ROOT/%_liconsdir
convert -size 48x48 gui/logo.xpm $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
convert -size 32x32 gui/logo.xpm $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 gui/logo.xpm $RPM_BUILD_ROOT/%_miconsdir/%name.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=GNUsound
Comment=%{Summary}
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GNOME;GTK;Audio;X-MandrivaLinux-Multimedia-Audio;
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README TODO CHANGES NOTES
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/omf/%{name}
%{_datadir}/gnome/apps/Multimedia/%name.desktop
%{_datadir}/gnome/help/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif


