Theoretically, QTIP has no dependency on installers or scenarios.

The following installers and scenarios have been validated in Danube release.

+------------------------+------------+-------------+
| Scenario               | Installer  | Validation  |
+========================+============+=============+
| os-odl_l2-nofeature-ha | Fuel@OPNFV | `zte-pod3`_ |
+------------------------+------------+-------------+
| os-nosdn-kvm-ha        | Fuel@OPNFV | `zte-pod1`_ |
+------------------------+------------+-------------+

See `configuration guide`_ for details

.. _Fuel@OPNFV: https://wiki.opnfv.org/display/fuel
.. _configuration guide: ../configguide
.. _zte-pod1: https://build.opnfv.org/ci/job/fuel-deploy-zte-pod1-daily-danube/
.. _zte-pod3: https://build.opnfv.org/ci/job/fuel-deploy-zte-pod3-daily-danube/