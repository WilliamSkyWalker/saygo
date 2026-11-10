"""Owned foreground window and desktop-focus oracle for the opt-in macOS test."""
import json
import os
import select
import sys

import AppKit as A
import Quartz as Q


def main():
    browser_pid = int(sys.argv[1])
    app = A.NSApplication.sharedApplication()
    app.setActivationPolicy_(A.NSApplicationActivationPolicyRegular)
    window = A.NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        ((100, 100), (500, 250)), A.NSWindowStyleMaskTitled, A.NSBackingStoreBuffered, False)
    window.setTitle_('Saygo focus regression fixture')
    label = A.NSTextField.labelWithString_('Browser operations must leave this window in front.')
    label.setFrame_(((25, 90), (450, 60)))
    window.contentView().addSubview_(label)
    app.finishLaunching()
    window.makeKeyAndOrderFront_(None)
    app.activateIgnoringOtherApps_(True)
    baseline = None
    changes = []

    def state():
        windows = Q.CGWindowListCopyWindowInfo(Q.kCGWindowListOptionOnScreenOnly, Q.kCGNullWindowID)
        order = [[int(w[Q.kCGWindowOwnerPID]), int(w[Q.kCGWindowNumber])]
                 for w in windows if w[Q.kCGWindowOwnerPID] in (os.getpid(), browser_pid)
                 and w[Q.kCGWindowLayer] == 0]
        return {'frontmost_pid': int(A.NSWorkspace.sharedWorkspace().frontmostApplication().processIdentifier()),
                'window_order': order, 'fixture_pid': os.getpid()}

    def reply(data):
        print(json.dumps(data), flush=True)

    reply({'ready': True, 'fixture_pid': os.getpid()})
    while True:
        event = app.nextEventMatchingMask_untilDate_inMode_dequeue_(
            A.NSEventMaskAny, A.NSDate.dateWithTimeIntervalSinceNow_(.02), A.NSDefaultRunLoopMode, True)
        if event is not None:
            app.sendEvent_(event)
        current = state()
        if baseline is not None and current != baseline and len(changes) < 20:
            if not changes or changes[-1] != current:
                changes.append(current)
        if select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline()
            if not line or line.strip() == 'quit':
                break
            command = line.strip()
            if command == 'mark':
                baseline, changes = current, []
            elif command == 'front':
                baseline, changes = None, []
                window.makeKeyAndOrderFront_(None)
                app.activateIgnoringOtherApps_(True)
            reply({'state': current, 'changes': changes})
    window.close()


if __name__ == '__main__':
    main()
