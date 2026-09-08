import pytest
import logging

from lib.vm import VM

# A playground to build KISS tests
#
#    Requirement:
#    - a host (--hosts=<IP>)
#    - a VM   (--vm=<UUID> or it uses PXE)



def test_vm_stop_start(imported_vm: VM) -> None:
    vm = imported_vm
    if (vm.is_running()):
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

    if (not vm.is_running):
        logging.info("VM is DOWN, starting it now ⌛")
        vm.start()

    vm.try_get_and_store_ip()
    vm.ssh_touch_file(tmp_file)
    assert vm.file_exists(tmp_file)

    vm.ssh(f"rm -f {tmp_file}")
    assert not vm.file_exists(tmp_file)