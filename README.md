# lbs-mono-fedora
Mono 4 packages for Fedora

See https://copr.fedoraproject.org/coprs/tpokorra/mono

# New packages
Package                        |Notes
-------------------------------|-----
gtk-sharp3                     |Epel6 missing gtk3
monodevelop-database           |Epel6 need fix mysql-connection-net first
mysql-connector-net            |Epel6 fail build when try apply patch0
notify-sharp3                  |Epel6 missing gtk3
npgsql                         |
nuget                          |
nunit                          |
nunit25                        |

# Dependecy list
Package                        |Run with Mono 4
-------------------------------|---------------
OpenTK                         |Work from Copr, EPEL6 need fix
RepetierHost                   |Need move to 4.5 profile
avahi-sharp                    |Need fix requires avahi-libs
banshee                        |Work from Copr, EPEL6 need fix libgpod first, EPEL7 missing gnome-desktop-devel
banshee-community-extensions   |Fedora package work without changes if Copr is configured
bareftp                        |Work from Copr
bless                          |Need move to 4.5 profile
boo                            |Need move to 4.5 profile
cdcollect                      |Need move to 4.5 profile
dbus-sharp                     |Work from Copr
dbus-sharp-glib                |Work from Copr
docky                          |Work from Copr, EPEL6 need fix gnome-keyring-sharp
gbrainy                        |Fedora package work without changes if Copr is configured
gdata-sharp                    |Work from Copr
gecko-sharp2                   |Need move to 4.5 profile
gio-sharp                      |Work from Copr
giver                          |Nedd fix avahi-sharp
gkeyfile-sharp                 |Work from Copr
gnome-desktop-sharp            |Work from Copr
gnome-do                       |Need move to 4.5 profile
gnome-guitar                   |Need move to 4.5 profile
gnome-keyring-sharp            |Work from Copr, Epel6 missing libgnome-keyring-devel
gnome-rdp                      |Need move to 4.5 profile
gnome-sharp                    |Work from Copr
gnome-subtitles                |Fedora package work without changes if Copr is configured
gsf-sharp                      |Need move to 4.5 profile
gtk-sharp-beans                |Work from Copr
gtk-sharp2                     |Work from Copr
gtksourceview-sharp            |Need move to 4.5 profile
gudev-sharp                    |Work from Copr
hyena                          |Work from Copr
keepass                        |Work from Copr for Fedora, EPEL need fixes
kimono                         |Need fix version requires of libmono-2.0.so.1
libappindicator		       |
libgpod                        |Work from Copr, EPEL6 need fix missing libusbx
log4net                        |Work from Copr
mono-addins                    |Work from Copr
mono-basic                     |Work from Copr. Updated to 4.0.1
mono-bouncycastle              |Need move to 4.5 profile
mono-cecil                     |Work from Copr
mono-cecil-flowanalysis        |Need move to 4.5 profile
mono-debugger                  |Need move to 4.5 profile
mono-reflection                |Need move to 4.5 profile
mono-tools                     |Need move to 4.5 profile
mono-zeroconf                  |Work from Copr
monobristol                    |Fedora package install without changes if Copr is configured
monodevelop                    |Work from Copr
monodevelop-debugger-gdb       |Fedora package install without changes if Copr is configured
monosim                        |Fedora package install without changes if Copr is configured
nant                           |Need mono(log4net) = 1.2.13.0
ndesk-dbus                     |Work from Copr
ndesk-dbus-glib                |Work from Copr
nini                           |Work from Copr
notify-sharp                   |Work from Copr
pdfmod                         |Need move to 4.5 profile
pinta                          |Fedora package work without changes if Copr is configured
poppler-sharp                  |Work from Copr
qyoto                          |Need move to 4.5 profile
rescene                        |
shogun                         |
sparkleshare                   |Fedora package work without changes if Copr is configured
syntastic                      |
taglib-sharp                   |Work from Copr
themonospot-base               |Need move to 4.5 profile
themonospot-console            |Need move to 4.5 profile
themonospot-gui-gtk            |Need move to 4.5 profile
themonospot-gui-qt             |Need move to 4.5 profile
themonospot-plugin-avi         |Need move to 4.5 profile
themonospot-plugin-mkv         |Need move to 4.5 profile
tomboy                         |Work from Copr
uwsgi                          |
webkit-sharp                   |Work from Copr
xsp                            |Work from Copr, EPEL6 need fix
