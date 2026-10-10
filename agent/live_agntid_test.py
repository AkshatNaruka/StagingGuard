"""Protected-only entrypoint for the verified StagingGuard proof."""
import sys
from stagingguard import main

if __name__ == "__main__":
    if "--phase" not in sys.argv:
        sys.argv.extend(["--phase", "after"])
    main()
