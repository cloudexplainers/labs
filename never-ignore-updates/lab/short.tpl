{{- range . }}{{ range .Vulnerabilities }}{{ .PkgName }}  {{ .VulnerabilityID }}  fixed in {{ .FixedVersion }}
{{ end }}{{ end -}}
