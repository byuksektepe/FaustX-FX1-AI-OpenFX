class key_sys:
    # For FX-1ALL AI
    def sys_def_keys(key, set_line_mode, set_lock_mode, aim_mode, lock_control, ift_proto):

        if (key == ord('l') or key == ord('L')):
            if (set_line_mode == False):
                set_line_mode = True
                print("Pressed Key [L], Line Tracking Enabled")

            else:
                set_line_mode = False
                print("Pressed Key [L], Line Tracking Disabled")
            return (0, set_line_mode)

        if (key == ord('O') or key == ord('o')):
            if (set_lock_mode == False):
                set_lock_mode = True
                print("Pressed Key [O], R-Lock Tracking Enabled")
            else:
                set_lock_mode = False
                print("Pressed Key [O], R-Lock Tracking Disabled")
            return (1, set_lock_mode)

        if (key == ord('0')):
            if (aim_mode == 0):
                aim_mode = 1
                print("Pressed Key [0]Zero, Aim Mode Sets Complex")
            else:
                aim_mode = 0
                print("Pressed Key [0]Zero, Aim Mode Sets Simple")
            return (2, aim_mode)

        if (key == ord('9')):
            if (lock_control == 0):
                lock_control = 1
                print("Pressed Key [9], Auto Lock Enabled")
            else:
                lock_control = 0
                print("Pressed Key [9], Auto Lock Disabled")
            return (3, lock_control)

        if (key == ord('i')):
            if (ift_proto == 0):
                ift_proto = 1
                print("Pressed Key [i], Target İdentify Protocol Enabled")
            else:
                ift_proto = 0
                print("Pressed Key [i], Target İdentify Protocol Disabled")
            return (4, ift_proto)
