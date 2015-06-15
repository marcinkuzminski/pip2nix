import pip
import pip.commands
import sys


def indent(amount, string):
    lines = string.splitlines() or ['']
    return lines[0] + '\n'.join(' ' * amount + l for l in lines[1:])


class NixFreezeCommand(pip.commands.InstallCommand):
    def run(self, options, args):
        options.no_install = True  # Download only
        options.upgrade = True  # Download all packages
        options.use_wheel = False  # We'll build the wheels ourself
        options.no_clean = True  # This is needed to access pkg_info later
        # TODO: what if InstallCommand.run fails?

        requirement_set = super(NixFreezeCommand, self).run(options, args)

        try:
            with open('python-packages.nix', 'w') as f:
                f.write('{')
                for req in requirement_set.requirements.values():
                    f.write(
                        self._generate_nix(req, requirement_set._dependencies[req]))
                f.write('}')
            return requirement_set
        finally:
            requirement_set.cleanup_files()

    def _generate_nix(self, requirement, deps):
        template = '\n'.join((
            '{name} = self.buildPythonPackage {{',
            '  doCheck = false;',  # TODO: tests
            '  name = "{name}-{version}";',
            '  src = {sourceExpr};',
            '  buildInputs = with self; [{buildInputs}];',
            '}};',
        ))

        link = requirement.link
        pkg_info = requirement.pkg_info()

        buildInputs = [d.name for d in deps]
        if link.scheme == 'file':
            sourceExpr = requirement.link.path
        elif link.scheme in ('http', 'https'):
            sourceExpr = '\n'.join((
                'fetchurl = {{',
                '  url = "{url}";',
                '  {hash_name} = "{hash}";',
                '}}'
            )).format(
                url=link.url,
                hash=link.hash,
                hash_name=link.hash_name,
            )

        return template.format(
            name=requirement.name,
            version=pkg_info['Version'],
            sourceExpr=indent(2, sourceExpr),
            buildInputs=' '.join(buildInputs)
        )


cmd = NixFreezeCommand()
sys.exit(cmd.main(sys.argv[1:]))
