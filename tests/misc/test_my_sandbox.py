import pytest
import logging
import time

from lib.vm import VM
from lib.vdi import VDI

# A playground to build KISS tests
#
#    Requirement:
#    - a host (--hosts=<IP>)
#    - a VM   (--vm=<UUID> or it uses PXE)


def test_vm_stop_start(imported_vm: VM) -> None:
    vm = imported_vm
    if vm.is_running():
        logging.info("VM already running, shutting it DOWN first ⌛")
        vm.shutdown(verify=True)
    logging.info("VM is DOWN, starting it now ⌛")
    vm.start()
    vm.wait_for_os_booted()
    logging.info("VM is UP ✅, shutting it DOWN again ⌛")

    vm.shutdown(verify=True)
    logging.info("VM is DOWN again ✅")
    vm.start()
    vm.wait_for_os_booted()
    logging.info("VM is UP again ✅")


def test_file_create_delete_on_vm(imported_vm: VM) -> None:
    vm = imported_vm
    tmp_file = f"/tmp/file_from-{test_file_create_delete_on_vm.__name__}"

    if not vm.is_running:
        logging.info("VM is DOWN, starting it now ⌛")
        vm.start()

    vm.try_get_and_store_ip()
    vm.ssh_touch_file(tmp_file)
    assert vm.file_exists(tmp_file)

    vm.ssh(f"rm -f {tmp_file}")
    assert not vm.file_exists(tmp_file)


def test_vdi_reset_on_boot_change(imported_vm: VM) -> None:
    """
    Provided test VM can be either booted or not
    VDI param "on-boot" will be rolled back
    """

    vm = imported_vm
    was_running = vm.is_running()
    vdi = VDI(vm.vdi_uuids()[0], host=vm.host)
    original_param_value = vdi.param_get("on-boot")

    if was_running:
        vm.shutdown(verify=True)

    if original_param_value == "persist":
        vdi.param_set("on-boot", "reset")
        vm.start()
        vm.wait_for_os_booted()

    tmp_file = f"/dummy-{int(time.time())}.tmp"
    vm.ssh_touch_file(tmp_file)
    assert vm.file_exists(tmp_file)

    vm.reboot(verify=True)
    assert not vm.file_exists(tmp_file)

    if original_param_value == "persist":
        logging.debug(f"Rollback to {original_param_value}")
        vm.shutdown(verify=True)
        vdi.param_set("on-boot", original_param_value)
        vm.start()
        vm.wait_for_os_booted()

    if not was_running:
        logging.debug(f"Shutdown VM (as initially provided)")
        vm.shutdown(verify=True)
