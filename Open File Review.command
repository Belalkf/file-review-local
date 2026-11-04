#!/bin/zsh
# Optional macOS launcher. Source use needs only the installed Python and Git.
cd -- "${0:A:h}" || exit 2
if (( $# == 0 )); then
  print 'Enter the Git repository root to review (or Control-C to cancel):'
  IFS= read -r target || exit 130
  [[ -n "$target" ]] || exit 2
  python3 -m file_review "$target"
else
  python3 -m file_review "$@"
fi
result=$?
if (( result != 0 )); then
  print '\nReview the warnings above. Press Return to close.'
  IFS= read -r
fi
exit "$result"
