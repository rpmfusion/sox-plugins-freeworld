%global realname sox

Summary:        Additional (free) codecs for sox
Name:           sox-plugins-freeworld
Version:        14.3.2
Release:        3%{?dist}
# sox.c is GPLv2, all other is LGPL2.1
License:        GPLv2+ and LGPLv2+
Group:          Applications/Multimedia

URL:            http://sox.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/sox/sox-%{version}.tar.gz
Patch0:         01-making-autoreconf-possible.patch
Patch1:         02-reconfigured-using-autoreconf.patch
Patch2:         03-adding-support-for-without-lpc.patch
Patch3:         04-nuking-libgsm-from-build-system.patch
Patch4:         06-fix-compile-error.patch
Patch5:         07-ignore-internal-libgsm.patch

BuildRequires:  libvorbis-devel
BuildRequires:  alsa-lib-devel, libtool-ltdl-devel, libsamplerate-devel
BuildRequires:  gsm-devel, wavpack-devel, ladspa-devel, libpng-devel
BuildRequires:  flac-devel, libao-devel, libsndfile-devel, libid3tag-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libtool
# Additional requirements for RPM Fusion
BuildRequires:  lame-devel ladspa-devel
BuildRequires:  libmad-devel
# Require Fedora package
Requires:       sox%{?_isa}

# No upstream exists and it has been moified by sox.
Provides: bundled(lpc10)


%description
SoX (Sound eXchange) is a sound file format converter SoX can convert
between many different digitized sound formats and perform simple
sound manipulation functions, including sound effects.

This package provides the plugin for MPEG-2 audio layer 3 audio (MP3) support.


%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
# Only appliy for ffmpeg 0.8 and above
%if %fedora >= 16
%patch4 -p1
%endif
%patch5 -p1

# Remove bundled libs
rm -rf libgsm
# lpc10 has no upstream so consider it a private lib.
# See http://lists.rpmfusion.org/pipermail/rpmfusion-developers/2012-March/012081.html
#rm -rf lpc10


%build
CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64"; export CFLAGS
autoreconf -if
%configure --enable-static=no \
           --with-dyn-default \
           --with-gsm=dyn \
           --includedir=%{_includedir}/sox \
           --with-distro=Fedora

#           --with-lpc10 \
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

# Remove all static libs
find %{buildroot}%{_libdir} -name "*.la" -exec rm -f {} \;

# Remove all the plugins execept the one we want.
find %{buildroot}%{_libdir}/sox -name "*.so" \! -name "*mp3.so" -exec rm -f {} \;

%files
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/sox/libsox_fmt_mp3.so
%exclude %{_bindir}
%exclude %{_datadir}
%exclude %{_includedir}
%exclude %{_libdir}/*.so*
%exclude %{_libdir}/pkgconfig


%changelog
* Thu Mar 22 2012 Richard Shaw <hobbes1069@gmail.com> - 14.3.2-3
- Add patches to deal with bundled libraries.

* Thu Mar 01 2012 Richard Shaw <hobbes1069@gmail.com> - 14.3.2-2
- Strip rpath from library.

* Sun Feb 26 2012 Richard Shaw <hobbes1069@gmail.com> - 14.3.2-1
- Initial Release.
