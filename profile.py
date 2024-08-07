#!/usr/bin/env python

#
# Standard geni-lib/portal libraries
#
import geni.portal as portal
import geni.rspec.pg as rspec
import geni.rspec.emulab as elab
import geni.rspec.igext as IG

tourDescription = """
.
"""

tourInstructions = "."

#
# Globals
#
class GLOBALS(object):
    SITE_URN = "urn:publicid:IDN+emulab.net+authority+cm"
    # Use kernel version required by free5gc: Ubuntu 18, kernel 5.0.0-23-generic
    UBUNTU22_IMG = "urn:publicid:IDN+utah.cloudlab.us+image+insaneproject-PG0:Ubuntu22.04-DPDK22.11"

    # default type
    HWTYPE = "d710"
    # SCRIPT_DIR = "/local/repository/scripts/"
    # SCRIPT_CONFIG = "setup-config"


# def invoke_script_str(filename):
#     # populate script config before running scripts (replace '?'s)
#     populate_config = "sed -i 's/NUM_UE_=?/NUM_UE_=" + str(params.uenum) + "/' " + GLOBALS.SCRIPT_DIR+GLOBALS.SCRIPT_CONFIG
#     populate_config2 = "sed -i 's/UERANSIM_BRANCHTAG_=?/UERANSIM_BRANCHTAG_=" + str(params.ueransim_branchtag) + "/' " + GLOBALS.SCRIPT_DIR+GLOBALS.SCRIPT_CONFIG
#     # also redirect all output to /script_output
#     run_script = "sudo bash " + GLOBALS.SCRIPT_DIR + filename + " &> ~/install_script_output"
#     return populate_config + " && " + populate_config2 + " && " +  run_script

#
# This geni-lib script is designed to run in the PhantomNet Portal.
#
pc = portal.Context()

#
# Create our in-memory model of the RSpec -- the resources we're going
# to request in our experiment, and their configuration.
#
request = pc.makeRequestRSpec()

# Optional physical type for all nodes.
pc.defineParameter("phystype",  "Optional physical node type",
                   portal.ParameterType.STRING, "d710",
                   longDescription="Specify a physical node type (d430,d740,pc3000,d710,etc) " +
                   "instead of letting the resource mapper choose for you.")

# pc.defineParameter("uenum","Number of simulated UEs to generate and register (0-10)",
#                    portal.ParameterType.INTEGER, 1, min=0, max=10)

# pc.defineParameter("ueransim_branchtag","Which tag/branch of UERANSIM to install",
#                    portal.ParameterType.STRING, "v3.2.0")


# Retrieve the values the user specifies during instantiation.
params = pc.bindParameters()
pc.verifyParameters()



gNBCoreLink = request.Link("gNBCoreLink")

# Add node which will run gNodeB and UE components with a simulated RAN.
sim_ran = request.RawPC("sim-ran")
sim_ran.component_manager_id = GLOBALS.SITE_URN
sim_ran.disk_image = GLOBALS.UBUNTU22_IMG
#sim_ran.docker_extimage = "ubuntu:20.04"
sim_ran.hardware_type = params.phystype 
# sim_ran.addService(rspec.Execute(shell="bash", command=invoke_script_str("ran.sh")))
gNBCoreLink.addNode(sim_ran)

# Add node that will host the 5G Core Virtual Network Functions (AMF, SMF, UPF, etc).
open5gs = request.RawPC("open5gs")
open5gs.component_manager_id = GLOBALS.SITE_URN
open5gs.disk_image = GLOBALS.UBUNTU22_IMG
#open5gs.docker_extimage = "ubuntu:20.04"
open5gs.hardware_type = GLOBALS.HWTYPE if params.phystype != "" else params.phystype
# open5gs.addService(rspec.Execute(shell="bash", command=invoke_script_str("open5gs.sh")))
gNBCoreLink.addNode(open5gs)

# Add node that will host Data Network
data_net = request.RawPC("Data-Network")
data_net.component_manager_id = GLOBALS.SITE_URN
data_net.disk_image = GLOBALS.UBUNTU22_IMG
data_net.hardware_type = GLOBALS.HWTYPE if params.phystype != "" else params.phystype
# data_net.addService(rspec.Execute(shell="bash", command=invoke_script_str("data_net.sh")))
gNBCoreLink.addNode(data_net)

tour = IG.Tour()
tour.Description(IG.Tour.MARKDOWN, tourDescription)
tour.Instructions(IG.Tour.MARKDOWN, tourInstructions)
request.addTour(tour)


pc.printRequestRSpec(request)
