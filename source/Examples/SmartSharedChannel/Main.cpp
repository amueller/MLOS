//*********************************************************************
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License. See License.txt in the project root
// for license information.
//
// @File: Main.cpp
//
// Purpose:
//      <description>
//
// Notes:
//      <special-instructions>
//
//*********************************************************************

#include "stdafx.h"

#include "MlosPlatform.Std.inl"

//----------------------------------------------------------------------------
// NAME: CheckHR
//
// PURPOSE:
//  Error checking.
//
// RETURNS:
//
// NOTES:
//  Terminates application in case of error.
//
void CheckHR(HRESULT hr)
{
    // Exceptional error handling.
    //
    if (FAILED(hr))
    {
        std::terminate();
    }
}

//----------------------------------------------------------------------------
// NAME: main
//
// PURPOSE:
//  Entertainment.
//
// RETURNS:
//
// NOTES:
//
int
__cdecl
main(
    __in int argc,
    __in char* argv[])
{
    UNUSED(argc);
    UNUSED(argv);

    // Create MlosContext.
    //
    Mlos::Core::InterProcessMlosContextInitializer mlosContextInitializer;
    HRESULT hr = mlosContextInitializer.Initialize();
    CheckHR(hr);

    Mlos::Core::InterProcessMlosContext mlosContext(std::move(mlosContextInitializer));

    // Configure feedback channel.
    //
    // hr = ConfigureFeedbackChannel(mlosContext);
    // CheckHR(hr);

    // Register Settings assemblies.
    // Must match GlobalDispatchTable.
    //
    hr = mlosContext.RegisterSettingsAssembly(
        "Mlos.UnitTest.SettingsRegistry.dll",
        Mlos::UnitTest::ObjectDeserializationHandler::DispatchTableBaseIndex());
    CheckHR(hr);

    hr = mlosContext.RegisterSettingsAssembly(
        "SmartSharedChannel.SettingsRegistry.dll",
        SmartSharedChannel::ObjectDeserializationHandler::DispatchTableBaseIndex());
    CheckHR(hr);

    // Register smart configs.
    //
    hr = RegisterSmartConfigs(mlosContext);
    CheckHR(hr);

    // Run the benchmark.
    //
    uint64_t messageCount = RunSharedChannelBenchmark(
        g_SharedChannelConfig,
        g_MicrobenchmarkConfig);
    (void)messageCount;
}
