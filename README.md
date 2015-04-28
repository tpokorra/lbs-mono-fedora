# lbs-mono-fedora
Mono 4 packages for Fedora

See https://copr.fedoraproject.org/coprs/tpokorra/mono

# New packages
Package                        |Notes
-------------------------------|-----
gtk-sharp3                     |Epel6 not ship gtk3
monodevelop-database           |Epel6 not build for mysql-connection-net dependency
mysql-connector-net            |Epel6 fail build when try apply patch0
notify-sharp3                  |Epel6 not ship gtk3
npgsql                         |
nuget                          |
nunit                          |

# Dependecy list
Package                        |Run with Mono 4
-------------------------------|---------------
OpenTK                         |Need move to 4.5 profile
RepetierHost                   |Need move to 4.5 profile
avahi-sharp                    |
banshee                        |Need fix version requires of mono(gkeyfile-sharp)
banshee-community-extensions   |Need fix banshe
bareftp                        |Need fix version requires of mono(Gnome.Keyring)
bless                          |Need move to 4.5 profile
boo                            |Need move to 4.5 profile
cdcollect                      |Need move to 4.5 profile
dbus-sharp                     |Work from Copr
dbus-sharp-glib                |Work from Copr
docky                          |Need fix requires of ndesk-dbus-glib
gbrainy                        |Fedora package work without changes if Copr is configured
gdata-sharp                    |Work from Copr
gecko-sharp2                   |
gio-sharp                      |Work from Copr
giver                          |Nedd fix avahi-sharp
gkeyfile-sharp                 |
gmime                          |
gnome-desktop-sharp            |Work from Copr
gnome-do                       |Need fix version requires of mono(NDesk.DBus.GLib)
gnome-guitar                   |Need move to 4.5 profile
gnome-keyring-sharp            |
gnome-rdp                      |Need fix version requires of mono(Gnome.Keyring)
gnome-sharp                    |Work from Copr
gnome-subtitles                |Fedora package work without changes if Copr is configured
graphviz                       |
gsf-sharp                      |
gtk-sharp-beans                |Work from Copr
gtk-sharp2                     |Work from Copr
gtksourceview-sharp            |
gudev-sharp                    |Work from Copr
hyena                          |Need move to 4.5 profile
keepass                        |Work from Copr for Fedora, EPEL need fixes
kimono                         |
libappindicator                |
libgpod                        |
log4net                        |Need move to 4.5 profile
mono-addins                    |Work from Copr
mono-basic                     |
mono-bouncycastle              |
mono-cecil-flowanalysis        |
mono-debugger                  |
mono-reflection                |
mono-tools                     |
mono-zeroconf                  |Work from Copr
monobristol                    |
monodevelop                    |Work from Copr
monodevelop-debugger-gdb       |
monosim                        |
nant                           |
ndesk-dbus                     |
ndesk-dbus-glib                |
nini                           |Need move to 4.5 profile
notify-sharp                   |Work from Copr
pdfmod                         |Need poppler-sharp
pinta                          |Fedora package work without changes if Copr is configured
poppler-sharp                  |Need move to 4.5 profile
python-elasticsearch           |
qyoto                          |Need move to 4.5 profile
rescene                        |
shogun                         |
sparkleshare                   |Fedora package work without changes if Copr is configured
syntastic                      |
taglib-sharp                   |
themonospot-base               |
themonospot-console            |
themonospot-gui-gtk            |
themonospot-gui-qt             |
themonospot-plugin-avi         |
themonospot-plugin-mkv         |
thrift                         |
tomboy                         |Work from Copr
uwsgi                          |
webkit-sharp                   |Work from Copr
xsp                            |Need move to 4.5 profile
