#
# spec file for package buildkit
#
# Copyright (c) 2024 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.


%global provider_prefix github.com/moby/buildkit
%global import_path     %{provider_prefix}
Name:           buildkit
Version:        0.18.2
Release:        1
Summary:        Toolkit for converting source code to build artifacts
License:        Apache-2.0
URL:            https://github.com/moby/buildkit
Source:         %{name}-%{version}.tar.zst
Source1:        vendor.tar.zst
Source2:        buildkit.service
BuildRequires:  containerd
BuildRequires:  runc
BuildRequires:  pkgconfig(systemd)
BuildRequires:  zstd
#BuildRequires:  golang(API) >= 1.13
BuildRequires:  golang(API) >= 1.23
Requires:       containerd
Requires:       runc

%description
BuildKit is a toolkit for converting source code to build artifacts in an efficient, expressive and repeatable manner.

%prep
%autosetup -a1 -n %{name}-%{version}/%{name}

%build
go build -mod=vendor -buildmode=pie -ldflags '-X %{import_path}/version.Version=%{version}' -o _output/buildkitd %{provider_prefix}/cmd/buildkitd
go build -mod=vendor -buildmode=pie -ldflags '-X %{import_path}/version.Version=%{version}' -o _output/buildctl %{provider_prefix}/cmd/buildctl

%install
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_unitdir}/
install -m 0755 _output/buildkitd %{buildroot}%{_bindir}/buildkitd
install -m 0755 _output/buildctl %{buildroot}%{_bindir}/buildctl
install -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/buildkit.service
install -m 0644 examples/systemd/system/buildkit.socket %{buildroot}%{_unitdir}/buildkit.socket

%pre
%service_add_pre buildkit.socket buildkit.service

%post
%service_add_post buildkit.socket buildkit.service

%preun
%service_del_preun buildkit.socket buildkit.service

%postun
%service_del_postun buildkit.socket buildkit.service

%files
%license LICENSE
%doc README.md docs/*.md
%{_bindir}/buildkitd
%{_bindir}/buildctl
%{_unitdir}/buildkit.socket
%{_unitdir}/buildkit.service
