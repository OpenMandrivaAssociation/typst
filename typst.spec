%global debug_package %{nil}

Name:		typst
Version:	0.14.0
Release:	1
Source0:	https://github.com/typst/typst/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:    %{name}-%{version}-vendor.tar.gz
Summary:	A new markup-based typesetting system that is powerful and easy to learn
URL:		https://github.com/typst/typst
License:	Apache-2.0
Group:		Terminal/Utility

BuildRequires:	cargo
BuildRequires:	pkgconfig(openssl)

%description
%summary.

%prep
%autosetup -p1
tar -zxf %{SOURCE1}
mkdir -p .cargo
cat >> .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source."git+https://github.com/typst/typst-dev-assets?tag=v0.14.0"]
git = "https://github.com/typst/typst-dev-assets"
tag = "v0.14.0"
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"

EOF

%build
cargo build --frozen --release

%install
cargo install --locked typst-cli --root %{buildroot}/usr --path ./crates/typst-cli
rm %{buildroot}/usr/.crate*

%files
%license LICENSE
%{_bindir}/%{name}
