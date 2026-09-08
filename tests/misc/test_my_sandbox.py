import pytest
import logging

from lib.vm import VM

# A playground to build KISS tests
#


def test_vm_stop_start(imported_vm: VM) -> None:
    """
    Requirement:
    - a host (--hosts=<IP>)
    - a VM   (--vm=<UUID> or it uses PXE)
    """

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